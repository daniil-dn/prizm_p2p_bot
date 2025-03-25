from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

withdraw_partner_balance = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывести вознаграждение', callback_data='withdraw_partner_balance')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_withdraw')]
], resize_keyboard=True)
