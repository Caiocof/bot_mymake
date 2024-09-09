import os

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.sql import func

# Configurações de conexão MySQL
DATABASE_URL = f'mysql+mysqlconnector://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'

# Criando a engine e a base declarativa
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Definição dos modelos
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
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
    client_name = Column(String(255))
    due_date = Column(DateTime)
    paid = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="sales")


# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)
