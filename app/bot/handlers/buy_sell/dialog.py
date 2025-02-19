from aiogram_dialog import Dialog
from app.bot.handlers.buy_sell.windows import get_value, get_wallet_info, orders_list

buy_sell_dialog = Dialog(
    get_value(),
    get_wallet_info(),
    orders_list()
)
