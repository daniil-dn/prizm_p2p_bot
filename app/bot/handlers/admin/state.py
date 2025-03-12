from aiogram.fsm.state import StatesGroup, State


class AdminSettingsState(StatesGroup):
    new_order_time = State()
    new_value_commission = State()
    new_pay_order_time = State()
    new_prizm_rate_diff_value = State()
    add_admin_by_username = State()
    remove_admin_by_username = State()
