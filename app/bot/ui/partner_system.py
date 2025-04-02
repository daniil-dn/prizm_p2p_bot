from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

withdraw_partner_balance = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывести вознаграждение', callback_data='withdraw_partner_balance')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_withdraw')]
], resize_keyboard=True)

def admin_withdrawal_done(user_id) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='✅Перевел(а)', callback_data=f'admin-done-partner-withdraw-request_{user_id}')

    builder = InlineKeyboardBuilder()
    builder.add(button)
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)

