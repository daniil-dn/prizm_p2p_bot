from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

withdraw_partner_balance = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывести вознаграждение', callback_data='withdraw_partner_balance')],
    [InlineKeyboardButton(text='Владельцам групп/каналов', callback_data='group_channel_owners')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_withdraw')]
], resize_keyboard=True)


def admin_withdrawal_done(user_id) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='✅Перевел(а)', callback_data=f'admin-done-partner-withdraw-request_{user_id}')

    builder = InlineKeyboardBuilder()
    builder.add(button)
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


cancel_partner_system = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='start_bot')]
], resize_keyboard=True)


accept_add_bot = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ бот добавлен в администраторы канала', callback_data='add_bot')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='start_bot')]
], resize_keyboard=True)
