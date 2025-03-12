from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from app.bot.handlers.admin.state import AdminSettingsState
from app.bot.middlewares.check_admin import check_admin
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('admin_panel_command'))
@check_admin
async def admin_menu_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                        dialog_manager: DialogManager) -> None:
    admin_command = cb.data.split('_')[-1]
    if admin_command == 'new-commission':
        await dialog_manager.start(state=AdminSettingsState.new_value_commission, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-order-wait-time':
        await dialog_manager.start(state=AdminSettingsState.new_order_time, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-pay-order-wait-time':
        await dialog_manager.start(state=AdminSettingsState.new_pay_order_time, mode=StartMode.RESET_STACK)
    elif admin_command == 'new-rate-diff':
        await dialog_manager.start(state=AdminSettingsState.new_prizm_rate_diff_value, mode=StartMode.RESET_STACK)

    elif admin_command == 'add-admin-by-username':
        await dialog_manager.start(state=AdminSettingsState.add_admin_by_username, mode=StartMode.RESET_STACK)

    elif admin_command == 'remove-admin-by-username':
        await dialog_manager.start(state=AdminSettingsState.remove_admin_by_username, mode=StartMode.RESET_STACK)
