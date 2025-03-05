from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.new_order.state import NewOrderState
from app.bot.ui import new_order_sell_buy_kb
from app.core.dao import crud_order, crud_user
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import User, Order

router = Router()


@router.callback_query(F.data.startswith('request_new_order'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession) -> None:
    text = "Продать или купить"
    await bot.send_message(cb.from_user.id, text, reply_markup=new_order_sell_buy_kb())


@router.callback_query(F.data.startswith('new_order_'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession, dialog_manager: DialogManager) -> None:
    await state.clear()
    mode = cb.data.split("_")[2]
    await dialog_manager.start(state=NewOrderState.from_value, mode=StartMode.RESET_STACK, data={"mode": mode})
