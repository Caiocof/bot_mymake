import sqlite3

from utils import truncate_text


def create_connection():
    connection = sqlite3.connect('estoque.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        buy_price REAL NOT NULL,
        sale_price REAL NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        payment_type TEXT NOT NULL,
        value REAL NOT NULL,
        name_client TEXT,
        due_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')

    connection.commit()


def connect_db():
    return sqlite3.connect('estoque.db')


def get_storage(id=None, quantity=None):
    connection = connect_db()
    cursor = connection.cursor()
    query = "SELECT id, name, quantity, sale_price FROM products"
    if id:
        query += f" WHERE id = {id}"
    elif quantity:
        query += f" WHERE quantity > {quantity}"
    cursor.execute(query)
    return cursor.fetchall()


def search_invoices_due():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name_client, value, due_date FROM sales WHERE payment_type = 'nota' AND date(due_date) <= date('now', '+2 days')")
    return cursor.fetchall()


def new_product(name, quantity, value_buy, value_sale):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO products (name, quantity, buy_price, sale_price) VALUES (?, ?, ?, ?)',
                   (name, int(quantity), float(value_buy), float(value_sale)))
    connection.commit()
    connection.close()


def update_product(product_id, name=None, quantity=None, value_buy=None, value_sale=None):
    connection = connect_db()
    cursor = connection.cursor()
    # Update dinamicamente apenas os campos fornecidos
    if name:
        cursor.execute("UPDATE products SET name = ? WHERE id = ?", (name, product_id))
    if quantity:
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (quantity, product_id))
    if value_buy:
        cursor.execute("UPDATE products SET buy_price = ? WHERE id = ?", (value_buy, product_id))
    if value_sale:
        cursor.execute("UPDATE products SET sale_price = ? WHERE id = ?", (value_sale, product_id))
    connection.commit()
    connection.close()


def new_sale(product_id, quantity, name_person, payment_type, due_date=None):
    connection = connect_db()
    try:
        quantity = int(quantity)
        cursor = connection.cursor()
        product = get_storage(id=product_id)[0]

        if not product or product[2] < quantity:
            return f"Quantidade em estoque é insuficiente:\nProduto: {product[1]}\nQnt. disponível: {product[2]}"

        cursor.execute(
            '''INSERT INTO sales 
            (product_id, quantity, name_client, payment_type,due_date,value) 
            VALUES (?,?, ?, ?,?,?)''',
            (int(product_id), quantity, name_person, payment_type, due_date, product[3]))

        new_quantity = product[2] - quantity
        cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        connection.commit()
        connection.close()
    except Exception as e:
        connection.rollback()
        return f'Erro ao registrar vendas: {e}'


def generate_reports_from_db(report_type: str):
    connection = connect_db()
    cursor = connection.cursor()

    if report_type == "sale_for_day":
        query = """
        SELECT created_at, SUM(sale_price) as total_sales
        FROM sales
        GROUP BY created_at
        ORDER BY created_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        report = "Não foi encontrado dados!\n"
        if rows:
            report = "Relatório de Vendas Diárias:\n"
            for row in rows:
                report += f"Data: {row[0]}, Total Vendas: R${row[1]:.2f}\n"

    elif report_type == "current_storage":
        query = """
        SELECT id, name, quantity, sale_price
        FROM products
        WHERE quantity > 0
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        report = "Não foi encontrado itens no estoque!\n"
        if rows:
            report = "Relatório de Estoque Atual:\n"
            report += "{:<6} | {:<15} | {:<6} | {:<10}\n".format("ID", "Nome", "Quant.", "Preço")
            report += "-" * 36 + "\n"
            for row in rows:
                name = truncate_text(row[1], 15)
                price = f"R${row[3]:.2f}"
                report += "{:<6} | {:<15} | {:<6} | {:<10}\n".format(row[0], name, row[2], price)
                report += "-" * 36 + "\n"

    else:
        report = "Tipo de relatório não reconhecido."

    connection.close()
    return report
