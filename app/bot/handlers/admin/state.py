from aiogram.fsm.state import StatesGroup, State


class AdminSettingsState(StatesGroup):
    new_order_time = State()
    new_value_commission = State()
    new_value_withdrawal_commission = State()
    new_pay_order_time = State()
    new_prizm_rate_diff_value = State()
    add_admin_by_username = State()
    remove_admin_by_username = State()


class GetHistoryMessage(StatesGroup):
    wait_for_id = State()


class UpdatePartnerPercent(StatesGroup):
    new_partner_percent = State()


class CreateMailing(StatesGroup):
    text_to_mailing = State()