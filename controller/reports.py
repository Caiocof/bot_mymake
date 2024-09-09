from datetime import datetime

from bot_config import BOT
from database.reports import generate_reports_current_storage, generate_reports_sale_for_day
from utils.utils import truncate_text


def get_current_storage(message, menu_button):
    try:
        rows = generate_reports_current_storage()
        report = rows
        if isinstance(rows, list):
            report = "Relatório de Estoque Atual:\n\n"
            for row in rows:
                name = truncate_text(row.name, 25)
                price = f"R${row.sale_price:.2f}"
                report += (f"<b>Código:</b> <code>{row.id}</code>\n"
                           f"<b>Nome:</b> <code>{name}</code>\n"
                           f"<b>Quant:</b> <code>{row.quantity}</code>\n"
                           f"<b>Preço:</b> <code>{price}</code>\n")
                report += "-" * 35 + "\n"
        BOT.send_message(message.from_user.id,
                         text=report,
                         parse_mode='html',
                         reply_markup=menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_sale_per_due_date(message, menu_button):
    try:
        rows = generate_reports_sale_for_day()
        report = rows
        if isinstance(rows, list):
            report = "✅Relatório de Vendas Diárias:\n\n"
            for row in rows:
                total = f"R${row.total_sales:.2f}"
                data_sale = row.created_at.strftime("%d-%m-%Y")
                report += (f"<b>Data:</b> <code>{data_sale}</code>\n"
                           f"<b>Valor Total:</b> <code>{total}</code>\n\n")
                report += "-" * 35 + "\n"
        BOT.send_message(message.from_user.id,
                         text=report,
                         parse_mode='html',
                         reply_markup=menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)
