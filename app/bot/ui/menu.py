from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def get_menu_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Купить Prizm', callback_data='mode_buy'),
            InlineKeyboardButton(text='Продать Prizm', callback_data='mode_sell'),

        ],
        [
            InlineKeyboardButton(text='Разместить Ордер', callback_data='new_order_request')
        ],
        [
            # InlineKeyboardButton(text='Профиль', callback_data='profile'),
            InlineKeyboardButton(text='Правила сервиса', callback_data='rules')
        ],
        [
            InlineKeyboardButton(text='Поддержка', callback_data='support')
        ],
        [
            InlineKeyboardButton(text='Перевести prizm в МойДом', callback_data='transfer_to_myhome')
        ]
    ]
    builder = InlineKeyboardBuilder(markup=buttons)
    return builder.as_markup()
