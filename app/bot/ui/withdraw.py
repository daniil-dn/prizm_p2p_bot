from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_withdraw = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_withdraw')]
], resize_keyboard=True)