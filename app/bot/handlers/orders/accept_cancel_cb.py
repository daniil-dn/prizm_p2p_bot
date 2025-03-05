from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import sent_card_transfer
from app.core.config import settings
from app.core.dao import crud_order, crud_user
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import User, Order

router = Router()


@router.callback_query(F.data.startswith('order_request_'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession) -> None:
    async with session:
        order = await crud_order.lock_row(session, id=int(cb.data.split('_')[3]))
        if order.status != Order.CREATED:
            await cb.message.edit_reply_markup(reply_markup=None)
            return

        # todo проверка времени
        if cb.data.split('_')[2] == "accept":
            if order.mode == "sell":
                await bot.send_message(
                    cb.from_user.id,
                    f"Вы подтвердили ордер. Ждем когда продавец переведет криптовалюту в Бота"
                )
                await bot.send_message(
                    order.to_user_id,
                    f"Ордер {order.id} подтвержден.\n Переведите криптовалюту на кошелек {settings.PRIZM_WALLET_ADDRESS} сумму: {order.from_value}\n Комментарий платежа: order:{order.to_user_id}:{order.id}"
                )
            else:
                from_user_wallet = await crud_wallet.get_by_user_id_currency(session, currency=order.to_currency,
                                                                             user_id=order.from_user_id)
                await bot.send_message(
                    order.to_user_id,
                    f"Переведите RUB на реквизиты {from_user_wallet.value}", reply_markup=sent_card_transfer(order.id)
                )
                await bot.send_message(
                    cb.from_user.id,
                    f"Ждите перевод RUB от пользователя"
                )

        else:
            order = await crud_order.update(session, db_obj=order, obj_in={"status": Order.CANCELED})
            user_db = await crud_user.lock_row(session, id=user_db.id)
            await crud_user.update(session, db_obj=user_db,
                                   obj_in={"cancel_order_count": user_db.cancel_order_count + 1})
            await bot.send_message(
                cb.from_user.id,
                "Отмена ордера, ваш рейтинг понижен"
            )
            await bot.send_message(
                order.to_user_id,
                f"Отмена ордера {order.id}"
            )
        await crud_order.update(session, db_obj=order, obj_in={"status": Order.ACCEPTED})
        await cb.message.edit_reply_markup(reply_markup=None)
