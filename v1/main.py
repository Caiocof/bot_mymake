import os

from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from controller import register_product, register_sale, register_full_sale, list_storage, check_invoices_due
from v1.db import create_connection

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AUTHORIZED_USERS = [920391928]

create_connection()


def get_menu_keyboard():
    keyboard = [
        [KeyboardButton("Cadastrar Produto")],
        [KeyboardButton("Registrar Vendas")],
        [KeyboardButton("Listar Estoque")],
        [KeyboardButton("Verificar Vencimentos do Dia")]
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


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if 'action' in context.user_data and context.user_data['action']:
        action = context.user_data['action']
        if action == 'register_product':
            await register_product(update, context, text)
        elif action == 'register_sale':
            await register_sale(update, context, text)
        elif action == 'register_full_sale':
            await register_full_sale(update, context, text)

    else:
        if text == "Cadastrar Produto":
            await update.message.reply_text(
                "Informe o nome do produto, quantidade, valor de compra e valor de venda (separados por vírgula):")
            context.user_data['action'] = 'register_product'
        elif text == "Registrar Vendas":
            await update.message.reply_text(
                "Informe o código do produto (id), quantidade, nome do cliente e forma de pagamento (cartão, dinheiro, pix ou nota):")
            context.user_data['action'] = 'register_sale'
        elif text == "Listar Estoque":
            await list_storage(update)
        elif text == "Verificar Vencimentos do Dia":
            await check_invoices_due(update)


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
