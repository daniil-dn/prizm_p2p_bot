from logging import getLogger

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.services.message_manager import MessageManager
from app.bot.ui import recieved_card_transfer, get_menu_kb
from app.bot.ui.order_seller_accept import contact_to_user
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order, crud_user
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import User, Order
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

router = Router()

logger = getLogger(__name__)


@router.callback_query(F.data.startswith('to_order_'))
async def accept_order_payment_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                  session: AsyncSession, message_manager: MessageManager) -> None:
    order_id = int(cb.data.split('_')[-1])
    data = await message_manager.get_message_and_keyboard(user_id=cb.from_user.id, order_id=order_id)
    message_id = data['message_id']

    message = await cb.message.answer(data['text'], reply_markup=data['keyboard'])

    try:
        await bot.edit_message_reply_markup(chat_id=cb.message.chat.id, message_id=message_id, reply_markup=None)
    except:
        pass

    await message_manager.set_message_and_keyboard(user_id=cb.from_user.id,
                                                   order_id=order_id,
                                                   text=data['text'],
                                                   keyboard=data['keyboard'],
                                                   message_id=message.message_id
                                                   )