from aiogram.fsm.state import StatesGroup, State


class GetMessage(StatesGroup):
    wait_for_message = State()