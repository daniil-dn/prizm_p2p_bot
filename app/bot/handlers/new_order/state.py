from aiogram.fsm.state import StatesGroup, State


class NewOrderState(StatesGroup):
    from_value = State()
    to_value = State()
    rate = State()
    sell_card_info = State()
