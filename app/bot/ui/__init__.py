from aiogram.types import ReplyKeyboardRemove

from .commands import get_default_commands
from .menu import get_menu_kb
from .profile import get_profile_kb
from .select_orders import get_select_orders_kb

remove = ReplyKeyboardRemove

__all__ = (
    "get_default_commands",
    "get_menu_kb",
    "get_profile_kb",
    "get_select_orders_kb"

)
