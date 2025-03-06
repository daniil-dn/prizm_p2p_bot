from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.callback_query(F.data.startswith('support'))
async def support_msg(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        """👉 https://t.me/Nikita_Kononenko"""
    )
