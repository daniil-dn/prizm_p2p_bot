from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def admin_panel_commot_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Получить историю сообщений по ID сделки', callback_data=f"admin_panel_command_message-history")
    builder.button(text='💰Изменить процент комиссии', callback_data=f"admin_panel_command_new-commission")
    builder.button(text='📊Изменить разницу курса',
                   callback_data=f"admin_panel_command_new-rate-diff")
    # todo добавить бота для проверки ордеров по времени
    builder.button(text='💳Изменить время ожидания оплаты', callback_data=f"admin_panel_command_new-pay-order-wait-time")
    builder.button(text='⏳Изменить время подтверждения ордера',
                   callback_data=f"admin_panel_command_new-order-wait-time")
    builder.button(text='🧑‍🏭Добавить админа',
                   callback_data=f"admin_panel_command_add-admin-by-username")
    builder.button(text='🗑Удалить админа',
                   callback_data=f"admin_panel_command_remove-admin-by-username")
    builder.button(text='🔙Назад',
                   callback_data=f"start_bot")

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
