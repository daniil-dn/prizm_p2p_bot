from aiogram.fsm.state import StatesGroup, State


class Withdraw(StatesGroup):
    get_count_money = State()
    get_prizm_address = State()


class ActivatePrizmWallet(StatesGroup):
    get_wallet = State()
