from aiogram.fsm.state import StatesGroup, State


class BuyState(StatesGroup):
    exact_value = State()
    card_details = State()
    orders_list = State()
    order_exact_value = State()
    order_confirmation = State()
    pay_card = State()
    success = State()
