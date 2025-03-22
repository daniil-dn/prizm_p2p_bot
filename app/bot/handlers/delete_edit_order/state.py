from aiogram.fsm.state import StatesGroup, State


class DeleteEditOrder(StatesGroup):
    orders = State()
    order_menu = State()
    update_menu = State()
    update_max_sum = State()
    update_min_sum = State()
    update_course = State()
