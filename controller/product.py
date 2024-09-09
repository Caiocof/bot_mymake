import re

from telebot.types import ForceReply

from bot_config import BOT
from database.products import new_product, get_product


def get_product_name(message, menu_button):
    try:
        msg = BOT.send_message(message.from_user.id,
                               text="<b>⚠️Qual o nome do produto?</b>",
                               parse_mode='html',
                               reply_markup=menu_button)
        BOT.register_next_step_handler(msg, get_quantity, menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_quantity(message, menu_button):
    try:
        product = {
            'name': message.text,
        }
        msg = BOT.send_message(message.from_user.id,
                               text="<b>⚠️Quantidade de itens?</b>",
                               parse_mode='html',
                               reply_markup=menu_button)
        BOT.register_next_step_handler(msg, get_buy_price, product, menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_buy_price(message, product, menu_button):
    try:
        force_reply = ForceReply()
        product['quantity'] = message.text

        if not product['quantity'].isdigit():
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>❌Quantidade invalida, insira um número.</b>",
                                   parse_mode="html",
                                   reply_markup=force_reply)
            BOT.register_next_step_handler(msg, get_buy_price, product, menu_button)
        else:
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>⚠️Qual o valor de compra?</b>",
                                   parse_mode="html",
                                   reply_markup=menu_button)
            BOT.register_next_step_handler(msg, get_sale_price, product, menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_sale_price(message, product, menu_button):
    try:
        force_reply = ForceReply()

        if not re.search(r'\d+[,.]\d{2}', message.text):
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>❌Valor invalido, formato esperado: 0,00!</b>",
                                   parse_mode="html",
                                   reply_markup=force_reply)
            BOT.register_next_step_handler(msg, get_sale_price, product, menu_button)
        else:
            product['buy_price'] = float(message.text.replace(",", "."))
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>⚠️Qual o valor de Venda?</b>",
                                   parse_mode="html",
                                   reply_markup=menu_button)
            BOT.register_next_step_handler(msg, save_product, product, menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def save_product(message, product, menu_button):
    try:
        force_reply = ForceReply()

        if not re.search(r'\d+[,.]\d{2}', message.text):
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>❌Valor invalido, formato esperado: 0,00!</b>",
                                   parse_mode="html",
                                   reply_markup=force_reply)
            BOT.register_next_step_handler(msg, save_product, product)
        else:
            try:
                product['sale_price'] = float(message.text.replace(",", "."))
                response = (f"<b>✅Produto cadastrado com sucesso!</b>\n"
                            f"<b>Nome:</b> <code>{product['name']}</code>\n"
                            f"<b>Quantidade:</b> <code>{product['quantity']}</code>\n"
                            f"<b>Valor de Compra:</b> <code>R$ {product['buy_price']}</code>\n"
                            f"<b>Valor de Venda:</b> <code>R$ {product['sale_price']}</code>")

                new_product(product)
                BOT.send_message(message.from_user.id,
                                 text=response,
                                 parse_mode='html',
                                 reply_markup=menu_button)
            except Exception as e:
                BOT.send_message(message.from_user.id,
                                 f"<b>❌Erro ao cadastrar produto: {e}</b>",
                                 parse_mode="html",
                                 reply_markup=menu_button)
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao cadastrar produto: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def check_quantity(product_id, quantity_sale):
    product = get_product(product_id)

    if not product:
        return "<b>❌Produto não encontrado.</b>"
    elif product.quantity < quantity_sale:
        return (f"<b>❌Quantidade em estoque é insuficiente:</b>\n"
                f"<b>Produto:</b> <code>{product.name}</code>\n"
                f"<b>Quantidade disponível:</b> <code>{product.quantity}</code>\n\n")
    return product
