from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💰 Купить | Продать PZM', callback_data='menu-mode-buy-sell'),
        ],
        [
            InlineKeyboardButton(text='💼 Личный кабинет', callback_data='personal')
        ],
        [
            InlineKeyboardButton(text='✉️ Поддержка', callback_data='support')
        ],
        [
            InlineKeyboardButton(text='🏨 Бот МойДом', url='https://t.me/MoyDom_Rielty_bot')
        ],
        [
            InlineKeyboardButton(text='⛏ Добыча PZM', url='https://t.me/Prizm_airdrop_bot')
        ],

    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel_menu')])
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)


def get_meny_buy_sell_mode_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💰 Купить PZM', callback_data='menu-mode-buy'),
            InlineKeyboardButton(text='₽ Продать PZM', callback_data='menu-mode-sell'),
        ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='start_bot')]
    ]
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)

def get_meny_buy_mode_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💰 Купить PZM сейчас', callback_data='mode-buy'),
        ],
        [
            InlineKeyboardButton(text='📋 Разместить ордер', callback_data='request_new_order')
        ],
        [
            InlineKeyboardButton(text='🔍 Все ордера на продажу', callback_data='mode-all_buy')
        ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='menu-mode-buy-sell')]
    ]
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)

def get_meny_sell_mode_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='₽ Продать PZM сейчас', callback_data='mode-sell'),
        ],
        [
            InlineKeyboardButton(text='📋 Разместить ордер', callback_data='request_new_order')
        ],
        [
            InlineKeyboardButton(text='🔍 Все ордера на покупку', callback_data='mode-all_sell')
        ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='menu-mode-buy-sell')]
    ]
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)



def get_menu_personal_area_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💼 Мои ордера', callback_data='my_order_requests')
        ],
        [
            InlineKeyboardButton(text='🤝 Партнерская программа', callback_data='partner_system')
        ],
        [
            InlineKeyboardButton(text='👛 Создать кошелек PZM', callback_data='create_wallet_prizm')
        ],
        [
            InlineKeyboardButton(text='👥 Владельцам групп/каналов', callback_data='group_channel_owners')
        ],
        [
            InlineKeyboardButton(text='🎓 Правила сервиса', callback_data='rules')
        ],
        [
            InlineKeyboardButton(text='Вывести PZM ➡️', callback_data='withdraw_balance')
        ],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='start_bot')]
    ]
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)


menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='start_bot')]
], resize_keyboard=True)
