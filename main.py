import os

from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from v1.db import create_connection
from controller import (
    register_product,
    register_sale,
    register_full_sale,
    list_storage,
    check_invoices_due,
    edit_product,
    edit_sale,
    generate_reports
)

load_dotenv()
create_connection()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USERS = [920391928, 7001706700]


def get_menu_keyboard():
    keyboard = [
        [KeyboardButton("Cadastrar Produto")],
        [KeyboardButton("Registrar Vendas")],
        [KeyboardButton("Listar Estoque")],
        [KeyboardButton("Verificar Vencimentos do Dia")],
        # [KeyboardButton("Editar Produto")],
        # [KeyboardButton("Gerar Relatórios")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True,
                               input_field_placeholder="Escolha uma opção")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("Você não está autorizado a usar este bot.")
        return
    reply_markup = get_menu_keyboard()
    await update.message.reply_text("Bem-vindo ao sistema de estoque! Escolha uma opção do menu:",
                                    reply_markup=reply_markup)


def get_back_to_menu_keyboard():
    keyboard = [
        [KeyboardButton("Voltar ao Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    reply_markup = get_back_to_menu_keyboard()

    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("Você não está autorizado a usar este bot.")
        return

    if 'action' in context.user_data and context.user_data['action']:
        action = context.user_data['action']
        if action == 'register_product':
            await register_product(update, context, text, reply_markup)
        elif action == 'register_sale':
            await register_sale(update, context, text, reply_markup)
        elif action == 'register_full_sale':
            await register_full_sale(update, context, text, reply_markup)
        elif action == 'edit_product':
            await edit_product(update, context, text, reply_markup)
        elif action == 'edit_sale':
            await edit_sale(update, context, text, reply_markup)
        elif action == 'generate_reports':
            await generate_reports(update, context, text, reply_markup)


    else:
        if text == "Cadastrar Produto":
            await update.message.reply_text(
                "Informe:\nnome do produto | quantidade | valor de compra | valor de venda:\n(separados por '/')")
            context.user_data['action'] = 'register_product'
        elif text == "Registrar Vendas":
            await update.message.reply_text(
                '''Informe:\ncódigo do produto (id) | quantidade | nome do cliente  | forma de pagamento 
                (cartão, dinheiro, pix ou nota):
                \n(separados por '/')''')
            context.user_data['action'] = 'register_sale'
        elif text == "Listar Estoque":

            await list_storage(update, reply_markup)
        elif text == "Verificar Vencimentos do Dia":
            await check_invoices_due(update, reply_markup)
            reply_markup = get_back_to_menu_keyboard()
            await update.message.reply_text("Ação concluída! Use o botão abaixo para voltar ao menu:",
                                            reply_markup=reply_markup)
        elif text == "Editar Produto":
            await update.message.reply_text(
                '''Informe o código do produto (id) e os novos valores 
                (nome | quantidade | valor de compra | valor de venda):
                \n(separados por '/')''')
            context.user_data['action'] = 'edit_product'
        elif text == "Editar Venda":
            await update.message.reply_text(
                '''Informe o código da venda (id) e os novos valores 
                (quantidade | nome do cliente | forma de pagamento):
                \n(separados por '/')''')
            context.user_data['action'] = 'edit_sale'
        elif text == "Gerar Relatórios":
            await update.message.reply_text(
                "Informe o tipo de relatório que deseja gerar:\n 1 - Estoque atual")
            context.user_data['action'] = 'generate_reports'
        elif text == "Voltar ao Menu":
            await start(update, context)
        else:
            await update.message.reply_text("Opção não reconhecida. Escolha uma opção do menu.")


async def menu(update: Update, context):
    await start(update, context)


def main():
    # Criar a aplicação
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adicionar os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar o bot
    application.run_polling()


if __name__ == '__main__':
    main()
