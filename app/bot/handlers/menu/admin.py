from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.ui import admin_panel_commot_kb
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('admin_panel_menu'))
async def admin_panel_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User) -> None:
    if user_db.role not in User.ALL_ADMINS:
        await bot.send_message(
            cb.from_user.id,
            f"Вы не админ!")
    await state.clear()
    await bot.send_message(cb.from_user.id, text="Вы в админ панели", reply_markup=admin_panel_commot_kb(is_main_admin=user_db.role == User.MAIN_ADMIN))
