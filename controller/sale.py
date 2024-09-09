import re
from datetime import datetime

from telebot.types import ForceReply

from bot_config import BOT
from controller.product import check_quantity
from database.products import get_product
from database.sales import new_sale
from utils.buttons import (
    get_back_to_menu_keyboard,
    get_sale_confirm_keyboard,
    get_payment_keyboard, add_new_item_keyboard
)

SALE_CONTEXT = {}


@BOT.callback_query_handler(func=lambda call: "action" in str(call))
def handle_action_callback(call):
    menu_button = get_back_to_menu_keyboard()
    try:
        action, response = call.data.split(":")
        current_user_data = SALE_CONTEXT[call.from_user.id]

        if response == "yes" and "payment_type" in current_user_data:
            response = new_sale(current_user_data)
            if response:
                BOT.send_message(call.from_user.id,
                                 text=response,
                                 parse_mode="html",
                                 reply_markup=menu_button)

            else:
                BOT.send_message(call.from_user.id,
                                 text="<b>✅Venda cadastrada com sucesso!</b>",
                                 parse_mode="html",
                                 reply_markup=menu_button)

        elif response == "yes":
            has_quantity = [check_quantity(item['product_id'],
                                           item['quantity']) for item in current_user_data['items']]

            if any(isinstance(item, str) for item in has_quantity):
                error_message = ''.join([item for item in has_quantity if isinstance(item, str)])
                SALE_CONTEXT[call.from_user.id] = {}
                BOT.send_message(call.from_user.id,
                                 text=error_message,
                                 parse_mode="html",
                                 reply_markup=menu_button)
            else:
                msg = BOT.send_message(call.from_user.id,
                                       text="<b>⚠️Inform o nome do cliente.</b>",
                                       parse_mode="html")

                BOT.register_next_step_handler(msg, get_client_name, menu_button)
        elif response == "no":
            sele_product(call, menu_button)
        elif response in ["card", "money", "pix", "check"]:

            current_user_data["payment_type"] = response

            if response == "check":
                msg = BOT.send_message(call.from_user.id,
                                       text="<b>⚠️Informe a data de vencimento 'DD-MM-YYYY':</b>",
                                       parse_mode="html")
                BOT.register_next_step_handler(msg, register_sale, menu_button)
            else:
                register_sale(call, menu_button)
    except Exception as e:
        SALE_CONTEXT[call.from_user.id] = {}
        BOT.send_message(call.from_user.id,
                         f"<b>❌Erro ao registrar uma venda (a): {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


@BOT.callback_query_handler(func=lambda call: "new_item" in str(call))
def handle_callback(call):
    menu_button = get_back_to_menu_keyboard()
    try:
        action, response = call.data.split(":")
        current_user_data = SALE_CONTEXT[call.from_user.id]
        if "yes" in response:
            return request_register_item(call.from_user.id, menu_button)

        text = f"<b>⚠️As informações estão corretas?</b>\n"
        for item in current_user_data['items']:
            text += (f"<b>Produto:</b> <code>{item['product_name']}</code>\n"
                     f"<b>Quantidade:</b> <code>{item['quantity']}</code>\n")
            text += "-" * 35 + "\n\n"

        BOT.send_message(call.from_user.id,
                         text=text,
                         parse_mode="html",
                         reply_markup=get_sale_confirm_keyboard())

    except Exception as e:
        BOT.send_message(call.from_user.id,
                         f"<b>❌Erro ao registrar uma venda (n.i): {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def sele_product(message, menu_button):
    try:
        SALE_CONTEXT[message.from_user.id] = {'items': []}
        return request_register_item(message.from_user.id, menu_button)

    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda (s.p): {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_product_code(message, menu_button):
    user_id = message.from_user.id
    force_reply = ForceReply()

    try:
        # Verifica o formato do input (esperado: '0,0')
        if not re.search(r'\d+,\d+', message.text):
            return request_correct_format(user_id, force_reply, menu_button)

        product_id, quantity = [item.strip() for item in message.text.split(",")]

        if not product_id.isdigit() or not quantity.isdigit():
            return request_valid_numbers(user_id, force_reply, menu_button)

        product_id = int(product_id)
        quantity = int(quantity)

        product = get_product(product_id)
        if not product:
            raise Exception("Produto não encontrado.")

        # if user_id not in SALE_CONTEXT:
        #     SALE_CONTEXT[user_id] = {'items': []}

        SALE_CONTEXT[user_id]['items'].append({
            "product_id": product_id,
            "product_name": product.name,
            "quantity": quantity
        })

        text = "<b>⚠️ Deseja adicionar um novo item?</b>\n"
        BOT.send_message(
            user_id,
            text=text,
            parse_mode="html",
            reply_markup=add_new_item_keyboard()
        )

    except Exception as e:
        SALE_CONTEXT[user_id] = {}
        BOT.send_message(
            user_id,
            f"<b>❌ Erro ao registrar uma venda (p.c): {e}</b>",
            parse_mode="html",
            reply_markup=menu_button
        )


def get_client_name(message, menu_button):
    try:
        SALE_CONTEXT[message.from_user.id]["client_name"] = message.text.upper()
        BOT.send_message(message.from_user.id,
                         text="<b>⚠️Escolha a forma de pagamento.</b>",
                         parse_mode="html",
                         reply_markup=get_payment_keyboard())
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda (c.n): {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def register_sale(message, menu_button):
    current_user_data = SALE_CONTEXT[message.from_user.id]
    try:
        payment_types = {
            "card": "Cartão",
            "money": "Dinheiro",
            "pix": "Pix",
            "check": "Nota"
        }
        payment = payment_types[current_user_data['payment_type']]

        text = ("<b>⚠️Informações da venda:</b>\n\n"
                f"<b>Nome do Cliente:</b> <code>{current_user_data['client_name']}</code>\n")
        text += "-" * 35 + "\n"
        for item in current_user_data['items']:
            product_name = item.pop("product_name")
            text += (f"<b>Produto:</b> <code>{product_name}</code>\n"
                     f"<b>Quantidade:</b> <code>{item['quantity']}</code>\n")
            text += "-" * 35 + "\n"

        if current_user_data['payment_type'] == "check":
            due_date = datetime.strptime(str(message.text), '%d-%m-%Y').date()
            current_user_data['due_date'] = due_date
            current_user_data['paid'] = False
            text += f"<b>Data de Vendimento:</b> <code>{message.text}</code>\n"

        text += (f"<b>Forma de Pagamento:</b> <code>{payment}</code>\n\n"
                 f"<b>As informações estão corretas?</b>")

        BOT.send_message(message.from_user.id,
                         text=text,
                         parse_mode="html",
                         reply_markup=get_sale_confirm_keyboard())
    except Exception as e:

        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda (r.s): {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def request_correct_format(user_id, force_reply, menu_button):
    msg = BOT.send_message(
        user_id,
        text="<b>❌ Valor inválido, formato esperado: 0,0!</b>",
        parse_mode="html",
        reply_markup=force_reply
    )
    BOT.register_next_step_handler(msg, get_product_code, menu_button)


def request_valid_numbers(user_id, force_reply, menu_button):
    msg = BOT.send_message(
        user_id,
        text="<b>❌ Código ou quantidade inválidos. Insira apenas números.</b>",
        parse_mode="html",
        reply_markup=force_reply
    )
    BOT.register_next_step_handler(msg, get_product_code, menu_button)


def request_register_item(user_id, menu_button):
    text = "<b>⚠️Digite o código do produto e quantidade:</b>\n<i>(separados por ',')</i>"
    msg = BOT.send_message(user_id,
                           text=text,
                           parse_mode="html",
                           reply_markup=menu_button)
    BOT.register_next_step_handler(msg, get_product_code, menu_button)
