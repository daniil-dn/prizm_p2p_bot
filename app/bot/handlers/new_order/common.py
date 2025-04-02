from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.services.message_manager import MessageManager
from app.bot.ui import get_menu_kb, contact_to_user
from app.bot.ui.texts import get_start_text
from app.bot.utils.accept_cancel import send_notification_to_actings
from app.core.dao import crud_order, crud_user, crud_order_request
from app.core.dto import OrderRequestUpdate
from app.core.models import User, Order, OrderRequest

router = Router()

@router.callback_query(F.data.startswith('pzm_sended_accept_order_request-'))
async def pzm_sended_accept_order_request_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                     session: AsyncSession, message_manager: MessageManager) -> None:
    await cb.message.edit_reply_markup(reply_markup=None)
    text = "⏳Ожидаем подтверждения перевода"
    await bot.send_message(cb.from_user.id, text)
