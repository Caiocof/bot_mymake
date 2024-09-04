import os

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func
from utils import truncate_text

# Configurações de conexão MySQL
DATABASE_URL = f'''mysql+mysqlconnector://
{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}
@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'''

# Criando a engine e a base declarativa
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Definição dos modelos
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    buy_price = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)

    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    payment_type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    name_client = Column(String(255))
    due_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="sales")


# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)


# Funções para interação com o banco de dados
def get_storage(id=None, quantity=None):
    session = SessionLocal()
    query = session.query(Product.id, Product.name, Product.quantity, Product.sale_price)

    if id:
        query = query.filter(Product.id == id)
    elif quantity:
        query = query.filter(Product.quantity > quantity)

    results = query.all()
    session.close()
    return results


def search_invoices_due():
    session = SessionLocal()
    results = session.query(Sale.name_client, Sale.value, Sale.due_date).filter(
        Sale.payment_type == 'nota',
        func.date(Sale.due_date) <= func.date(func.now() + func.interval('2', 'DAY'))
    ).all()
    session.close()
    return results


def new_product(name, quantity, value_buy, value_sale):
    session = SessionLocal()
    new_product = Product(name=name, quantity=quantity, buy_price=value_buy, sale_price=value_sale)
    session.add(new_product)
    session.commit()
    session.close()


def update_product(product_id, name=None, quantity=None, value_buy=None, value_sale=None):
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()

    if product:
        if name:
            product.name = name
        if quantity:
            product.quantity = quantity
        if value_buy:
            product.buy_price = value_buy
        if value_sale:
            product.sale_price = value_sale
        session.commit()

    session.close()


def new_sale(product_id, quantity, name_person, payment_type, due_date=None):
    session = SessionLocal()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()

        if not product or product.quantity < quantity:
            session.close()
            return f'''Quantidade em estoque é insuficiente:\n
            Produto: {product.name}\n
            Qnt. disponível: {product.quantity}'''

        sale = Sale(product_id=product_id, quantity=quantity,
                    name_client=name_person, payment_type=payment_type,
                    due_date=due_date, value=product.sale_price)
        product.quantity -= quantity

        session.add(sale)
        session.commit()
    except Exception as e:
        session.rollback()
        return f'Erro ao registrar vendas: {e}'
    finally:
        session.close()


def generate_reports_from_db(report_type: str):
    session = SessionLocal()

    if report_type == "sale_for_day":
        query = session.query(Sale.created_at, func.sum(Sale.quantity * Product.sale_price).label('total_sales')).join(
            Product).group_by(Sale.created_at).order_by(Sale.created_at.desc())
        rows = query.all()
        report = "Não foi encontrado dados!\n"
        if rows:
            report = "Relatório de Vendas Diárias:\n"
            for row in rows:
                report += f"Data: {row.created_at}, Total Vendas: R${row.total_sales:.2f}\n"

    elif report_type == "current_storage":
        query = session.query(Product.id, Product.name, Product.quantity, Product.sale_price).filter(
            Product.quantity > 0)
        rows = query.all()
        report = "Não foi encontrado itens no estoque!\n"
        if rows:
            report = "Relatório de Estoque Atual:\n"
            report += "{:<6} | {:<15} | {:<6} | {:<10}\n".format("ID", "Nome", "Quant.", "Preço")
            report += "-" * 36 + "\n"
            for row in rows:
                name = truncate_text(row.name, 15)
                price = f"R${row.sale_price:.2f}"
                report += "{:<6} | {:<15} | {:<6} | {:<10}\n".format(row.id, name, row.quantity, price)
                report += "-" * 36 + "\n"

    else:
        report = "Tipo de relatório não reconhecido."

    session.close()
    return report
