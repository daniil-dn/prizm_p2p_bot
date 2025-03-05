from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from app.core.models import User
from app.bot.handlers.buy_sell.state import BuyState

router = Router()


@router.callback_query(F.data.startswith('mode_'))
async def buy_sell_mode_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                           dialog_manager: DialogManager) -> None:
    await state.clear()
    mode = cb.data.split('_')[1]
    await dialog_manager.start(state=BuyState.from_value, mode=StartMode.RESET_STACK, data={"mode": mode})
