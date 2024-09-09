from datetime import datetime

from telebot.types import ForceReply

from bot_config import BOT
from controller.product import check_quantity
from database.products import get_product
from database.sales import new_sale
from utils.buttons import get_back_to_menu_keyboard, get_sale_confirm_keyboard, get_payment_keyboard

SALE_CONTEXT = {}


@BOT.callback_query_handler(func=lambda call: "action" in str(call))
def handle_action1_callback(call):
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
            has_quantity = check_quantity(current_user_data['product_id'],
                                          current_user_data['quantity'])
            if isinstance(has_quantity, str):
                BOT.send_message(call.from_user.id,
                                 text=has_quantity,
                                 parse_mode="html",
                                 reply_markup=menu_button)
            else:
                msg = BOT.send_message(call.from_user.id,
                                       text="<b>⚠️Inform o nome do cliente.</b>",
                                       parse_mode="html")

                BOT.register_next_step_handler(msg, get_client_name, menu_button)
        elif response == "no":
            current_user_data = {}
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
        BOT.send_message(call.from_user.id,
                         f"<b>❌Erro ao registrar uma venda: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def sele_product(message, menu_button):
    try:
        text = "<b>⚠️Digite o código do produto e quantidade:</b>\n<i>(separados por ',')</i>"
        msg = BOT.send_message(message.from_user.id,
                               text=text,
                               parse_mode="html",
                               reply_markup=menu_button)
        BOT.register_next_step_handler(msg, get_product_code, menu_button)

    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_product_code(message, menu_button):
    try:
        force_reply = ForceReply()
        product_id, quantity = [item.strip() for item in message.text.split(",")]

        if not product_id.isdigit() or not quantity.isdigit():
            msg = BOT.send_message(message.from_user.id,
                                   text="<b>❌Código ou quantidade invalidos, insira números.</b>",
                                   parse_mode="html",
                                   reply_markup=force_reply)
            BOT.register_next_step_handler(msg, get_product_code, menu_button)
        else:
            product_id = int(product_id)
            product = get_product(product_id)

            if not product:
                raise Exception('Produto não encontrado.')

            SALE_CONTEXT[message.from_user.id] = {"product_id": product_id,
                                                  "product_name": product.name,
                                                  "quantity": int(quantity)
                                                  }
            texto = (f"<b>⚠️As informações estão corretas?</b>\n"
                     f"<b>Produto:</b> <code>{product.name}</code>\n"
                     f"<b>Quantidade:</b> <code>{int(quantity)}</code>")
            BOT.send_message(message.from_user.id,
                             text=texto,
                             parse_mode="html",
                             reply_markup=get_sale_confirm_keyboard())
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def get_client_name(message, menu_button):
    try:
        SALE_CONTEXT[message.from_user.id]["client_name"] = message.text.upper()
        BOT.send_message(message.from_user.id,
                         text="<b>⚠️Escolha a forma de pagamento.</b>",
                         parse_mode="html",
                         reply_markup=get_payment_keyboard())
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)


def register_sale(message, menu_button):
    try:
        current_user_data = SALE_CONTEXT[message.from_user.id]

        payment_types = {
            "card": "Cartão",
            "money": "Dinheiro",
            "pix": "Pix",
            "check": "Nota"
        }
        payment = payment_types[current_user_data['payment_type']]
        product_name = current_user_data.pop("product_name")
        texto = (f"<b>⚠️Informações da venda:</b>\n"
                 f"<b>Produto:</b> <code>{product_name}</code>\n"
                 f"<b>Quantidade:</b> <code>{current_user_data['quantity']}</code>\n"
                 f"<b>Nome do Cliente:</b> <code>{current_user_data['client_name']}</code>\n")

        if current_user_data['payment_type'] == "check":
            due_date = datetime.strptime(str(message.text), '%d-%m-%Y').date()
            current_user_data['due_date'] = due_date
            current_user_data['paid'] = False
            texto += f"<b>Data de Vendimento:</b> <code>{message.text}</code>\n"

        texto += (f"<b>Forma de Pagamento:</b> <code>{payment}</code>\n\n"
                  f"<b>As informações estão corretas?</b>")
        BOT.send_message(message.from_user.id,
                         text=texto,
                         parse_mode="html",
                         reply_markup=get_sale_confirm_keyboard())
    except Exception as e:
        BOT.send_message(message.from_user.id,
                         f"<b>❌Erro ao registrar uma venda: {e}</b>",
                         parse_mode="html",
                         reply_markup=menu_button)
