from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.models import ChatChannel

withdraw_partner_balance = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вывести вознаграждение', callback_data='withdraw_partner_balance')],
    [InlineKeyboardButton(text='Владельцам групп/каналов', callback_data='group_channel_owners')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='personal')]
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
    [InlineKeyboardButton(text='✅ Я добавил бота', callback_data='add_bot')],
    [InlineKeyboardButton(text='❌ Отмена', callback_data='group_channel_owners')]
], resize_keyboard=True)

owners_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить канал/группу', callback_data='add_channel')],
    [InlineKeyboardButton(text='Мои группы/каналы', callback_data='my_channels')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='partner_system')]
], resize_keyboard=True)

success_add_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои группы/каналы', callback_data='my_channels')],
    [InlineKeyboardButton(text='🔙Назад', callback_data='partner_system')]
], resize_keyboard=True)


def update_chats(chats: list[ChatChannel]):
    kb = InlineKeyboardBuilder()
    for chat in chats:
        kb.button(text=f'✅ {chat.username or chat.name or chat.id}', callback_data=f'update_{chat.id}')

    kb.button(text='🔙Назад', callback_data='partner_system')
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def cancel_to_select_option(chat: ChatChannel):
    kb = InlineKeyboardBuilder()
    kb.button(text=f'❌ Отмена', callback_data=f'update_{chat.id}')

    return kb.as_markup(resize_keyboard=True)

def update_chat_options(chat: ChatChannel):
    kb = InlineKeyboardBuilder()
    kb.button(text='Кол-во в день', callback_data='count_in_day')
    kb.button(text='Время между постами', callback_data='interval')
    kb.button(text='Интервал в течение дня', callback_data='interval_in_day')

    if chat.is_stopped:
        kb.button(text='▶️продолжить постинг', callback_data='continue_posting')
    else:
        kb.button(text='⏸️Остановить постинг', callback_data='stop_posting')

    kb.button(text='❌ Отмена', callback_data='my_channels')

    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def url_button(link: str):
    kb = InlineKeyboardBuilder()
    kb.button(text='👉 ПЕРЕЙТИ В БОТА', url=link)


    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
