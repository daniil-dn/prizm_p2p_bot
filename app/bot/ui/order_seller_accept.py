from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def order_seller_accept_kb(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Принять ордер', callback_data=f"order_request_accept_{order_id}")
    builder.button(text='❌ Отказаться', callback_data=f"order_request_cancel_{order_id}")
    return builder.as_markup()


def sent_card_transfer(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Оплатил', callback_data=f"sent_card_transfer_{order_id}")
    # builder.button(text='❌ Отмена', callback_data=f"cancel_card_transfer_{order_id}")
    return builder.as_markup()


def recieved_card_transfer(order_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✅ Получил', callback_data=f"card_transfer_recieved_{order_id}")
    # builder.button(text='❌ Отмена', callback_data=f"cancel_card_transfer_{order_id}")
    return builder.as_markup()
