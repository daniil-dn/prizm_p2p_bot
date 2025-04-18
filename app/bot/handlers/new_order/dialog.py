from aiogram_dialog import Dialog
from app.bot.handlers.new_order.windows import get_from_value, get_to_value, get_rate, get_sell_card_info, \
    get_wallet_method

new_order_dialog = Dialog(
    get_from_value(),
    get_to_value(),
    get_rate(),
    get_wallet_method(),
    get_sell_card_info()
)
