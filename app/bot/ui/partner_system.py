from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

withdraw_partner_balance = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывести вознаграждение', callback_data='withdraw_partner_balance')]
], resize_keyboard=True)