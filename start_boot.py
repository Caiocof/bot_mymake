import os

from bot_config import BOT
from controller.product import get_product_name
from controller.receivable import get_receivable
from controller.reports import get_current_storage, get_sale_per_due_date
from controller.sale import sele_product
from utils.buttons import get_menu_keyboard, get_back_to_menu_keyboard


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    BOT.reply_to(message, "Bem-vindo ao sistema de estoque!\n /menu para ver as opções do sistema")


@BOT.message_handler(commands=['menu'])
def show_menu(message):
    markup = get_menu_keyboard()
    BOT.send_message(message.from_user.id, "Escolha o que deseja fazer!", reply_markup=markup)


@BOT.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    menu_button = get_back_to_menu_keyboard()
    if call.data == "menu":
        show_menu(call)
    elif call.data == "new_product":
        get_product_name(call, menu_button)
    elif call.data == "new_sale":
        sele_product(call, menu_button)
    elif call.data == "get_storage":
        get_current_storage(call, menu_button)
    elif call.data == "seal_for_day":
        get_sale_per_due_date(call, menu_button)
    elif call.data == "receivable_accounts":
        get_receivable(call, menu_button)


if __name__ == '__main__':
    print(f"Start bot")
    BOT.infinity_polling()
