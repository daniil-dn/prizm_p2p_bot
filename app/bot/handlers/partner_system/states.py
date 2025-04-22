from aiogram.fsm.state import StatesGroup, State


class WithdrawPartner(StatesGroup):
    get_count_money = State()
    get_prizm_address = State()


class AddChannel(StatesGroup):
    get_chat_channel_id = State()
    get_count_in_day = State()
    accept = State()
    get_interval = State()
    get_interval_in_day = State()


class UpdateChannel(StatesGroup):
    select_chat = State()
    select_option = State()
    count_in_day = State()
    interval = State()
    interval_in_day = State()
