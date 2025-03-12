from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.ui import get_menu_kb
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('support'))
async def support_msg(message: Message, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()
    await bot.send_message(
        message.from_user.id,
        """👉 https://t.me/Nikita_Kononenko""", reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
    )
