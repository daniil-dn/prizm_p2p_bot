from aiogram_dialog import Dialog
from app.bot.handlers.buy_sell.windows import get_from_value, get_to_value, get_wallet_info, orders_list, \
    get_exactly_value

buy_sell_dialog = Dialog(
    get_from_value(),
    get_to_value(),
    get_wallet_info(),
    orders_list(),
    get_exactly_value()
)
