from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Главное меню', callback_data='start_bot')]
], resize_keyboard=True)
