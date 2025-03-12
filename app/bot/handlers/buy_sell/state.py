from aiogram.fsm.state import StatesGroup, State


class BuyState(StatesGroup):
    exact_value = State()
    card_method_details = State()
    wallet_details = State()
    orders_list = State()
    accept_order_request = State()
