from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def order_seller_accept_kb(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Принять ордер', callback_data=f"order_request_accept_{order_id}")
    builder.button(text='❌ Отказаться', callback_data=f"order_request_cancel_{order_id}")
    return builder.as_markup(resize_keyboard=True)


def sent_card_transfer(order, user_id=None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Оплатил', callback_data=f"sent_card_transfer_{order.id}")
    builder.button(text='💬Поддержка', url="https://t.me/Nikita_Kononenko")
    if user_id:
        button = _get_contact_user_button(user_id, order)
        builder.add(button)

    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def recieved_card_transfer(order, user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Получил', callback_data=f"card_transfer_recieved_{order.id}")
    builder.button(text='💬Поддержка', url="https://t.me/Nikita_Kononenko")
    if user_id:
        button = _get_contact_user_button(user_id, order)
        builder.add(button)


    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

def _get_contact_user_button(user_id, order):
    if order.mode == "buy":
        if order.to_user_id == user_id:
            user_seller = False
        else:
            user_seller = True
    else:
        if order.to_user_id == user_id:
            user_seller = True
        else:
            user_seller = False
    if user_seller:
        button_text = '🔗Связаться с продавцом🔗'
    else:
        button_text = '🔗Связаться с покупателем🔗'

    return InlineKeyboardButton(text=button_text, callback_data=f'contact_{user_id}_{order.id}')


def contact_to_user(user_id, order) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.add(_get_contact_user_button(user_id, order))
    builder.button(text='К сделке', callback_data=f'to_order_{order.id}')
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


cancel_contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отменить', callback_data='cancel_contact')]
], resize_keyboard=True)
