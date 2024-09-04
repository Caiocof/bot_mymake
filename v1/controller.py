from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from db import search_invoices_due, new_product, new_sale, sale_with_check, update_product, \
    generate_reports_from_db


async def register_product(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
    try:
        name, quantity, valeu_buy, value_sale = map(str.strip, text.split('/'))
        new_product(name, quantity, valeu_buy, value_sale)
        context.user_data['action'] = None
        await update.message.reply_text(f"Produto '{name}' cadastrado com sucesso!", reply_markup=markup)
    except Exception as e:
        context.user_data['action'] = None
        await update.message.reply_text(f"Erro ao cadastrar produto: {e}")


async def edit_product(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
    try:
        name, quantity, valeu_buy, value_sale = map(str.strip, text.split('/'))
        update_product(name, quantity, valeu_buy, value_sale)
        context.user_data['action'] = None
        await update.message.reply_text(f"Produto '{name}' editado com sucesso!", reply_markup=markup)
    except Exception as e:
        context.user_data['action'] = None
        await update.message.reply_text(f"Erro ao editar produto: {e}")


async def register_sale(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
    try:
        product_id, quantity, name_person, payment_type = map(str.strip, text.split('/'))
        if payment_type.lower() == 'nota':
            await update.message.reply_text(
                "Informe a data de vencimento 'DD-MM-YYYY':")
            context.user_data['register_sale'] = (product_id, quantity, name_person,)
            context.user_data['action'] = 'register_full_sale'
        else:
            response = new_sale(product_id, quantity, name_person, payment_type)
            context.user_data['action'] = None
            message = "Venda registrada com sucesso!"
            if response:
                message = response
            await update.message.reply_text(message, reply_markup=markup)
    except Exception as e:
        context.user_data['action'] = None
        await update.message.reply_text(f"Erro ao registrar venda: {e}")


async def register_full_sale(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, markup):
    try:

        due_date = map(str.strip, text.split(','))
        due_date = datetime.strptime(str(due_date), '%d-%m-%Y')
        product_id, quantity, name_person = context.user_data['register_sale']

        response = sale_with_check(product_id, quantity, name_person, due_date)
        context.user_data['action'] = None
        message = "Venda registrada com sucesso!"
        if response:
            message = response
        await update.message.reply_text(message, reply_markup=markup)
    except Exception as e:
        context.user_data['action'] = None
        await update.message.reply_text(f"Erro ao registrar venda: {e}")


async def list_storage(update: Update, markup):
    try:
        report = generate_reports_from_db('current_storage')

        await update.message.reply_text(report, reply_markup=markup)
    except Exception as e:
        await update.message.reply_text(f"Erro ao listar estoque: {e}")


async def check_invoices_due(update: Update, markup):
    try:
        sales = search_invoices_due()
        response = "Nenhuma conta a vencer nos próximos dias!"
        if sales:
            response = "Vencimentos próximos:\n"
            for sele in sales:
                response += f"Nome: {sele[0]}, Vencimento: {sele[1]}\n"
        await update.message.reply_text(response, reply_markup=markup)
    except Exception as e:
        await update.message.reply_text(f"Erro ao verificar vencimentos: {e}")
