from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.models import ChatChannel

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
    [InlineKeyboardButton(text='❌ Отмена', callback_data='group_channel_owners')]
], resize_keyboard=True)

cancel_to_my_channels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌ Отмена', callback_data='my_channels')]
], resize_keyboard=True)


accept_add_bot = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ бот добавлен в администраторы канала', callback_data='add_bot')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='start_bot')]
], resize_keyboard=True)


owners_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить канал/группу', callback_data='add_channel')],
    [InlineKeyboardButton(text='Мои группы/каналы', callback_data='my_channels')],
    [InlineKeyboardButton(text='Назад', callback_data='partner_system')]
], resize_keyboard=True)

success_add_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои группы/каналы', callback_data='my_channels')],
    [InlineKeyboardButton(text='Назад', callback_data='partner_system')]
], resize_keyboard=True)


def update_chats(chats: list[ChatChannel]):
    kb = InlineKeyboardBuilder()
    for chat in chats:
        kb.button(text=f'✅ {chat.username or chat.name or chat.id}', callback_data=f'update_{chat.id}')

    kb.button(text='Назад', callback_data='partner_system')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


update_chat_options = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кол-во в день', callback_data='count_in_day')],
    [InlineKeyboardButton(text='Время между постами', callback_data='interval')],
    [InlineKeyboardButton(text='Интервал в течение дня', callback_data='interval_in_day')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='my_channels')]
], resize_keyboard=True)
