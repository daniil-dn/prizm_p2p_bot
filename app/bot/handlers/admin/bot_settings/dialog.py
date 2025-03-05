from aiogram_dialog import Dialog
from app.bot.handlers.admin.bot_settings.windows import get_new_wait_order_time, get_new_commission_value

admin_bot_settings_dialog = Dialog(
    get_new_wait_order_time(),
    get_new_commission_value(),
)
