from database.config import SessionLocal, Product


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


def new_product(data: dict):
    try:
        session = SessionLocal()
        product = Product(**data)

        session.add(product)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
        raise e


def update_product(product_id, name=None, quantity=None, value_buy=None, value_sale=None):
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()

    if product:
        if name:
            product.name = name
        if quantity is not None:
            product.quantity = quantity
        if value_buy is not None:
            product.buy_price = value_buy
        if value_sale is not None:
            product.sale_price = value_sale
        session.commit()

    session.close()


def get_product(product_id):
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        return product
    return None
