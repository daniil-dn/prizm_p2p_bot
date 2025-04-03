from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💰 Купить PZM', callback_data='mode-buy'),
            InlineKeyboardButton(text='₽ Продать PZM', callback_data='mode-sell'),
        ],
        [
            InlineKeyboardButton(text='📋 Разместить ордер', callback_data='request_new_order')
        ],
        [
            InlineKeyboardButton(text='🔍 Все ордера на покупку', callback_data='mode-all_sell')
        ],
        [
            InlineKeyboardButton(text='🔍 Все ордера на продажу', callback_data='mode-all_buy')
        ],
        [
            InlineKeyboardButton(text='💼 Мои ордера', callback_data='my_order_requests')
        ],
        [
            InlineKeyboardButton(text='🤝 Партнерская программа', callback_data='partner_system')
        ],
        [
            InlineKeyboardButton(text='🎓 Правила сервиса', callback_data='rules')
        ],
        [
            InlineKeyboardButton(text='✉️ Поддержка', callback_data='support')
        ],
        [
            InlineKeyboardButton(text='Вывести PZM ➡️', callback_data='withdraw_balance')
        ],
        [
            InlineKeyboardButton(text='🏨 Перевести PZM в МойДом', callback_data='transfer_to_myhome')
        ]
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel_menu')])
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup(resize_keyboard=True)


menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='start_bot')]
], resize_keyboard=True)
