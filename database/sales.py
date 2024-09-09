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
        new_data = [
            {'product_id': item['product_id'],
             'quantity': item['quantity'],
             'client_name': data['client_name'],
             'payment_type': data['payment_type']}
            for item in data['items']
        ]

        with session.begin():
            for item in new_data:
                product_id = item['product_id']
                product = get_product(product_id)

                sale = Sale(**item)
                sale.value = product.sale_price
                session.add(sale)

                new_quantity = product.quantity - item['quantity']
                update_product(product_id, quantity=new_quantity)

            session.commit()

    except Exception as e:
        session.rollback()
        raise Exception(f'<b>❌DB Erro: {e}</b>')

    finally:
        session.close()
