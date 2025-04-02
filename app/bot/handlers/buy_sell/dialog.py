from aiogram_dialog import Dialog
from app.bot.handlers.buy_sell.windows import get_wallet_info, orders_list, \
    get_accept_order, get_value, get_wallet_method

buy_sell_dialog = Dialog(
    get_value(),
    get_wallet_method(),
    get_wallet_info(),
    orders_list(),
    get_accept_order()
)
