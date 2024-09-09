from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Cadastrar Produto", callback_data="new_product"),
        InlineKeyboardButton("Registrar Vendas", callback_data="new_sale"),
        InlineKeyboardButton("Vencimentos do Dia", callback_data="seal_for_day"),
        InlineKeyboardButton("Vendas a Vencer", callback_data="receivable_accounts"),
        InlineKeyboardButton("Listar Estoque", callback_data="get_storage"),
    )
    return markup


def get_back_to_menu_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Menu", callback_data="menu"))
    return markup


def get_sale_confirm_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Sim", callback_data="action:yes"),
        InlineKeyboardButton("Não", callback_data="action:no"))
    return markup


def add_new_item_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Sim", callback_data="new_item:yes"),
        InlineKeyboardButton("Não", callback_data="new_item:no"))
    return markup


def get_payment_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Cartão", callback_data="action:card"),
        InlineKeyboardButton("Dinheiro", callback_data="action:money"),
        InlineKeyboardButton("Pix", callback_data="action:pix"),
        InlineKeyboardButton("Nota", callback_data="action:check")
    )
    return markup
