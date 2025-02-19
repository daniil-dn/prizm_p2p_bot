from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.models import User
from ..ui import get_menu_kb

router = Router()


@router.message(CommandStart())
@router.message(Command("start"))
async def start_cmd(message: Message, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()
    await bot.send_message(
        # todo + обработка партнерских ссылок
        message.from_user.id,
        f"""Привет это команда start
         
Ваш баланс: {user_db.balance}
Кол-во сделок: {user_db.order_count}
Кол-во отказов: {user_db.cancel_order_count}
""",
        reply_markup=get_menu_kb()
    )
