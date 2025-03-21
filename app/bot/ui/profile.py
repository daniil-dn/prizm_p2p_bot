from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_profile_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Изменить адрес prizm', callback_data="change_prizm_address")
    builder.button(text='Изменить реквизиты карты', callback_data="change_card_info")
    return builder.as_markup(resize_keyboard=True)
