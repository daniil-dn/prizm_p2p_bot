from aiogram_dialog import Dialog
from app.bot.handlers.admin.bot_settings.windows import (get_new_wait_order_time, get_new_commission_value,
                                                         get_prizm_rate_diff_value, get_pay_order_time_value,
                                                         add_admin_by_username, remove_admin_by_username)

admin_bot_settings_dialog = Dialog(
    get_new_wait_order_time(),
    get_new_commission_value(),
    get_pay_order_time_value(),
    get_prizm_rate_diff_value(),
    add_admin_by_username(),
    remove_admin_by_username(),
)
