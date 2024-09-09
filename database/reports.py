from sqlalchemy import func

from database.config import SessionLocal, Sale, Product
from utils.utils import truncate_text


def generate_reports_sale_for_day():
    session = SessionLocal()
    try:
        query = session.query(Sale.created_at,
                              func.sum(Sale.quantity * Product.sale_price).label('total_sales')).join(
            Product).group_by(Sale.created_at).order_by(Sale.created_at.desc())
        rows = query.all()

        if not rows:
            return "<b>⚠️Não foi encontrado dados de venda para o período.</b>\n"
        return rows
    except Exception as e:
        session.rollback()
        raise Exception(f'Não foi possível buscar relatório: {e}')
    finally:
        session.close()


def generate_reports_current_storage():
    session = SessionLocal()
    try:
        query = session.query(Product.id, Product.name, Product.quantity, Product.sale_price).filter(
            Product.quantity > 0)
        rows = query.all()

        if not rows:
            return "<b>⚠️Não foi encontrado itens no estoque!</b>\n"
        return rows
    except Exception as e:
        session.rollback()
        raise Exception(f'Não foi possível buscar relatório: {e}')
    finally:
        session.close()


def receivable_account():
    session = SessionLocal()
    try:
        query = (session.query(Sale.client_name,
                               Sale.due_date,
                               func.sum(Sale.quantity * Product.sale_price).label('total_sales'))
                 .join(Product)
                 .group_by(Sale.client_name, Sale.due_date)
                 .order_by(Sale.due_date.desc()))
        rows = query.all()

        if not rows:
            return "<b>⚠️Não foi encontrado vendas parceladas!</b>\n"
        return rows
    except Exception as e:
        session.rollback()
        raise Exception(f'Não foi possível buscar relatório: {e}')
    finally:
        session.close()
