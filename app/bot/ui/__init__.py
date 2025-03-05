from aiogram.types import ReplyKeyboardRemove

from .commands import get_default_commands
from .menu import get_menu_kb
from .profile import get_profile_kb
from .order_seller_accept import order_seller_accept_kb, sent_card_transfer, recieved_card_transfer
from .new_order import new_order_sell_buy_kb
from .admin import admin_panel_commot_kb

remove = ReplyKeyboardRemove

__all__ = (
    "get_default_commands",
    "get_menu_kb",
    "get_profile_kb",
    "order_seller_accept_kb",
    "new_order_sell_buy_kb",
    "admin_panel_commot_kb",
    "sent_card_transfer",
    "recieved_card_transfer"
)
