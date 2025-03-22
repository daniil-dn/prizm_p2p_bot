from aiogram_dialog import Dialog

from .windows import get_orders, get_order_menu, update_menu_order, update_min_sum_order, update_max_sum_order, \
    update_cource_order, delete_order_window

router = Dialog(
    get_orders(),
    get_order_menu(),
    update_menu_order(),
    update_min_sum_order(),
    update_max_sum_order(),
    update_cource_order(),
    delete_order_window(),
)
