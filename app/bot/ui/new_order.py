from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def new_order_sell_buy_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💰Покупка Prizm', callback_data=f"new_order_buy")
    builder.button(text='₽ Продажа Prizm', callback_data=f"new_order_sell")
    return builder.as_markup(resize_keyboard=True)
