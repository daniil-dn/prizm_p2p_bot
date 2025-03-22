from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from app.bot.handlers.delete_edit_order.state import DeleteEditOrder
from app.core.models import User
from app.bot.handlers.buy_sell.state import BuyState

router = Router()


@router.callback_query(F.data.startswith('my_order_requests'))
async def buy_sell_mode_cb(cb: CallbackQuery, state: FSMContext,
                           dialog_manager: DialogManager) -> None:
    await state.clear()
    await dialog_manager.start(state=DeleteEditOrder.orders, mode=StartMode.RESET_STACK)
