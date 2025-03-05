from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from app.core.models import User
from ..ui import get_menu_kb

router = Router()


@router.message(CommandStart())
@router.message(Command("start"))
async def start_cmd(message: Message, command: CommandObject, bot: Bot, state: FSMContext, user_db: User) -> None:
    args = command.args
    if args:
        start_data = decode_payload(args)
        if start_data == "myhomeref":
            await message.answer("Вы перешли из МойДом!")

    await state.clear()
    s = await state.get_state()
    await bot.send_message(
        # todo + обработка партнерских ссылок
        user_db.id,
        f"""Привет это команда start
Ваш баланс: {user_db.balance}
Кол-во сделок: {user_db.order_count}
Кол-во отказов: {user_db.cancel_order_count}
""",
        reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
    )
