from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.ui import get_menu_kb
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('transfer_to_myhome'))
async def transfer_to_myhome_msg(message: Message, bot: Bot, state: FSMContext, user_db: User) -> None:
    await state.clear()
    await bot.send_message(
        # todo
        message.from_user.id,
        """Тут ссылка будет""", reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
    )
