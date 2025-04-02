from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from ..ui import get_menu_kb
from ..ui.texts import get_start_text
from ...core.dao import crud_user
from ...core.dto import UserCreate

router = Router()


@router.message(CommandStart())
async def start_cmd_message(message: Message, bot: Bot, state: FSMContext, user_db: User | None, command: CommandObject,
                            dialog_manager: DialogManager, session: AsyncSession) -> None:
    if not user_db:
        partner_id = int(command.args, 16) if command.args else None
        create_user_data = UserCreate(
            id=message.from_user.id,
            language_code=message.from_user.language_code,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            partner_id=partner_id
        )
        user_db = await crud_user.create(session, obj_in=create_user_data)
    await dialog_manager.reset_stack(remove_keyboard=True)
    await state.clear()
    await bot.send_message(
        user_db.id, get_start_text(user_db.balance, user_db.order_count, user_db.cancel_order_count),
        reply_markup=get_menu_kb(is_admin=user_db.role in User.ALL_ADMINS)
    )


@router.callback_query(F.data.startswith('start_bot'))
@router.callback_query(F.data == ('cancel_withdraw'))
async def start_cmd_cb(callback: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                       dialog_manager: DialogManager, session: AsyncSession) -> None:
    await dialog_manager.reset_stack(remove_keyboard=True)
    await state.clear()
    await bot.send_message(
        user_db.id, get_start_text(user_db.balance, user_db.order_count, user_db.cancel_order_count),
        reply_markup=get_menu_kb(is_admin=user_db.role in User.ALL_ADMINS)
    )