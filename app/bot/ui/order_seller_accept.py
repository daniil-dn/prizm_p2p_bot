from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def order_seller_accept_kb(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Принять ордер', callback_data=f"order_request_accept_{order_id}")
    builder.button(text='❌ Отказаться', callback_data=f"order_request_cancel_{order_id}")
    return builder.as_markup(resize_keyboard=True)


def sent_card_transfer(order_id, user_id = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Оплатил', callback_data=f"sent_card_transfer_{order_id}")
    builder.button(text='💬Поддержка', url="https://t.me/Nikita_Kononenko")
    if user_id:
        builder.button(text='связаться', callback_data=f'contact_{user_id}_{order_id}')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def recieved_card_transfer(order_id, user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Получил', callback_data=f"card_transfer_recieved_{order_id}")
    builder.button(text='💬Поддержка', url="https://t.me/Nikita_Kononenko")
    builder.button(text='связаться', callback_data=f'contact_{user_id}_{order_id}')

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def contact_to_user(user_id, order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='связаться', callback_data=f'contact_{user_id}_{order_id}')

    return builder.as_markup(resize_keyboard=True)


cancel_contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel_contact')]
], resize_keyboard=True)