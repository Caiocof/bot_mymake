from sqlalchemy import func

from database.config import SessionLocal, Sale
from database.products import get_product, update_product


def search_invoices_due():
    session = SessionLocal()
    results = session.query(Sale.client_name, Sale.value, Sale.due_date).filter(
        Sale.payment_type == 'check',
        func.date(Sale.due_date) <= func.date(func.now() + func.interval('2', 'DAY'))
    ).all()
    session.close()
    return results


def new_sale(data: dict):
    session = SessionLocal()
    try:
        product_id = data['product_id']
        product = get_product(product_id)

        sale = Sale(**data)
        sale.value = product.sale_price

        session.add(sale)
        session.commit()

        new_quantity = product.quantity - data['quantity']
        update_product(product_id, quantity=new_quantity)
    except Exception as e:
        session.rollback()
        raise Exception(f'<b>❌Erro ao registrar vendas: {e}</b>')
    finally:
        session.close()
