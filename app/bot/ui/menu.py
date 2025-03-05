from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_menu_kb(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='💰 Купить Prizm', callback_data='mode_buy'),
            InlineKeyboardButton(text='₽ Продать Prizm', callback_data='mode_sell'),

        ],
        [
            InlineKeyboardButton(text='📋 Разместить ордер', callback_data='request_new_order')
        ],
        [
            InlineKeyboardButton(text='📋 Правила сервиса', callback_data='rules')
        ],
        [
            InlineKeyboardButton(text='✉️ Поддержка', callback_data='support')
        ],
        [
            InlineKeyboardButton(text='🏨 Перевести prizm в МойДом', callback_data='transfer_to_myhome')
        ]
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton(text='Админ-панель', callback_data='admin_panel_menu')])
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup()
