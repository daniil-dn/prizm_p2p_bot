from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def admin_panel_commot_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💰Изменить процент комиссии', callback_data=f"admin_panel_command_new-commission")
    builder.button(text='📊Изменить разницу курса',
                   callback_data=f"admin_panel_command_new-rate-diff")
    # todo добавить бота для проверки ордеров по времени
    builder.button(text='💳Изменить время ожидания оплаты', callback_data=f"admin_panel_command_new-pay-order-wait-time")
    builder.button(text='⏳Изменить время подтверждения ордера',
                   callback_data=f"admin_panel_command_new-order-wait-time")
    builder.button(text='🔙Назад',
                   callback_data=f"start_bot")

    builder.adjust(1)
    return builder.as_markup()
