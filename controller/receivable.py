from bot_config import BOT
from database.reports import receivable_account


def get_receivable(message, menu_button):
    try:
        rows = receivable_account()
        report = rows
        if isinstance(rows, list):
            report = "✅Relatório de vendas a receber:\n\n"
            for row in rows:
                print(row)
                total = f"R${row.total_sales:.2f}"
                due_date = row.due_date.strftime("%d-%m-%Y")
                report += (f"<b>Client:</b> <code>{row.client_name}</code>\n"
                           f"<b>Valor Total:</b> <code>{total}</code>\n"
                           f"<b>Data Vencimento:</b> <code>{due_date}</code>\n")
                report += "-" * 35 + "\n"
        BOT.send_message(message.from_user.id,
                         text=report,
                         parse_mode='html',
                         reply_markup=menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao buscar vendas a receber: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)
