from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('profile'))
async def profile_msg(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()

    await bot.send_message(
        cb.from_user.id,
        f"""
Ваш баланс: {user_db.balance}
Кол-во сделок: {user_db.order_count}
Кол-во отказов: {user_db.cancel_order_count}
        """
    )
