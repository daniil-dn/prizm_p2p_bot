from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot.ui import admin_panel_commot_kb
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('admin_panel_menu'))
async def admin_panel_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    if user_db.role != User.ADMIN_ROLE:
        await bot.send_message(
            cb.from_user.id,
            f"Вы не админ!")
    await state.clear()
    await bot.send_message(cb.from_user.id, text="Вы в админ панели", reply_markup=admin_panel_commot_kb())
