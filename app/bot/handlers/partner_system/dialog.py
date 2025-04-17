from aiogram_dialog import Dialog

from app.bot.handlers.partner_system.windows import get_chats, get_options, update_count_in_day, update_interval_window, \
    update_interval_in_day_window

router = Dialog(get_chats(), get_options(), update_count_in_day(), update_interval_window(), update_interval_in_day_window())
