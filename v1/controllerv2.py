# from datetime import datetime
#
# from telegram import Update
# from telegram.ext import ContextTypes
#
# from utils import truncate_text
# from database.db import (
#     search_invoices_due,
#     new_product,
#     new_sale,
#     update_product,
#     generate_reports_from_db
# )
#
#
# async def register_product(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     try:
#         name, quantity, valeu_buy, value_sale = map(str.strip, text.split('/'))
#         new_product(name, quantity, valeu_buy, value_sale)
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Produto '{name}' cadastrado com sucesso!", reply_markup=markup)
#     except Exception as e:
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Erro ao cadastrar produto: {e}")
#
#
# async def edit_product(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     try:
#         name, quantity, valeu_buy, value_sale = map(str.strip, text.split('/'))
#         update_product(name, quantity, valeu_buy, value_sale)
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Produto '{name}' editado com sucesso!", reply_markup=markup)
#     except Exception as e:
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Erro ao editar produto: {e}")
#
#
# async def register_sale(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     try:
#         product_id, quantity, name_person, payment_type = map(str.strip, text.split('/'))
#         if payment_type.lower() == 'nota':
#             await update.message.reply_text(
#                 "Informe a data de vencimento 'DD-MM-YYYY':")
#             context.user_data['register_sale'] = (product_id, quantity, name_person, payment_type)
#             context.user_data['action'] = 'register_full_sale'
#         else:
#             response = new_sale(product_id, quantity, name_person, payment_type)
#             context.user_data['action'] = None
#             message = "Venda registrada com sucesso!"
#             if response:
#                 message = response
#             await update.message.reply_text(message, reply_markup=markup)
#     except Exception as e:
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Erro ao registrar venda: {e}")
#
#
# async def register_full_sale(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     try:
#         due_date = datetime.strptime(str(text), '%d-%m-%Y')
#         product_id, quantity, name_person, payment_type = context.user_data['register_sale']
#
#         response = new_sale(product_id, quantity, name_person, payment_type, due_date)
#         context.user_data['action'] = None
#         message = "Venda registrada com sucesso!"
#         if response:
#             message = response
#         await update.message.reply_text(message, reply_markup=markup)
#     except Exception as e:
#         context.user_data['action'] = None
#         await update.message.reply_text(f"Erro ao registrar venda: {e}")
#
#
# async def list_storage(update: Update, markup):
#     try:
#         report = generate_reports_from_db('current_storage')
#
#         await update.message.reply_text(report, reply_markup=markup)
#     except Exception as e:
#         await update.message.reply_text(f"Erro ao listar estoque: {e}")
#
#
# async def check_invoices_due(update: Update, markup):
#     try:
#         sales = search_invoices_due()
#         report = "Nenhuma conta a vencer nos próximos dias!"
#         if sales:
#             report = "Vencimentos próximos:\n"
#             for row in sales:
#                 name = truncate_text(row[0], 25)
#                 price = f"R${row[1]:.2f}"
#                 due_data = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
#                 report += f"Nome: {name}\nValor: {price}\nVencimento: {due_data.strftime('%d-%m-%Y')}\n"
#                 report += "-" * 30 + "\n"
#         await update.message.reply_text(report, reply_markup=markup)
#     except Exception as e:
#         await update.message.reply_text(f"Erro ao verificar vencimentos: {e}")
#
#
# async def edit_sale(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     # Exemplo de formato de entrada: "ID da venda, nova quantidade, novo nome do cliente, nova forma de pagamento"
#     data = text.split('/')
#     try:
#         if len(data) == 4:
#             sale_id = data[0].strip()
#             new_quantity = int(data[1].strip())
#             new_client_name = data[2].strip()
#             new_payment_method = data[3].strip()
#             print(sale_id, new_quantity, new_client_name, new_payment_method)
#             await update.message.reply_text("Venda atualizada com sucesso!", reply_markup=markup)
#         else:
#             await update.message.reply_text("Formato inválido. Tente novamente.")
#     except Exception as e:
#         await update.message.reply_text(f"Erro ao editar venda: {e}")
#
#
# async def generate_reports(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
#     # Função para gerar relatórios
#     report_type = text.strip()
#     report_type = 'current_storage' if '1' in report_type else 'sale_for_day'
#     report = generate_reports_from_db(report_type)
#     await update.message.reply_text(report, reply_markup=markup)
#
#
# async def search_products(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
#     # Função para buscar produtos
#     search_query = text.strip()
#     results = print(search_query)
#     results_str = "\n".join([f"ID: {p[0]}, Nome: {p[1]}, Quantidade: {p[2]}, Preço: {p[3]}" for p in results])
#     await update.message.reply_text(f"Resultados da pesquisa:\n{results_str}")
