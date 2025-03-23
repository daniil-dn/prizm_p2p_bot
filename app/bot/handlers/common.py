from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.core.models import User
from ..ui import get_menu_kb
from ..ui.texts import get_start_text

router = Router()


@router.message(CommandStart())
@router.message(Command("start"))
@router.callback_query(F.data.startswith('start_bot'))
@router.callback_query(F.data == ('cancel_withdraw'))
async def start_cmd(message: Message, bot: Bot, state: FSMContext, user_db: User,
                    dialog_manager: DialogManager) -> None:
    await dialog_manager.reset_stack(remove_keyboard=True)
    await state.clear()
    await bot.send_message(
        user_db.id, get_start_text(user_db.balance, user_db.order_count, user_db.cancel_order_count),
        reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
    )
