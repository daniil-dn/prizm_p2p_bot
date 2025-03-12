from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import sent_card_transfer, get_menu_kb
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order, crud_user, crud_settings, crud_order_request
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import OrderRequestUpdate
from app.core.models import User, Order, OrderRequest

router = Router()


@router.callback_query(F.data.startswith('order_request_'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession) -> None:
    async with session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
        order = await crud_order.lock_row(session, id=int(cb.data.split('_')[3]))
        if order.status != Order.CREATED:
            await cb.message.edit_reply_markup(reply_markup=None)
            return

        if cb.data.split('_')[2] == "accept":
            if order.mode == "sell":
                await bot.send_message(
                    cb.from_user.id,
                    f"Вы подтвердили ордер. Ждем когда продавец переведет криптовалюту в Бота"
                )
                prizm_with_commission = order.prizm_value + order.prizm_value * order.commission_percent
                await bot.send_message(
                    order.to_user_id,
                    f"Ордер №{order.id} подтвержден.\n"
                    f"Переведите {prizm_with_commission} PZM c коммиссией сервиса {order.commission_percent * 100}%\n"
                    f"Без комментария платеж потеряется!\n"
                    f"На кошелек сервиса: <b>{settings.PRIZM_WALLET_ADDRESS}</b>\n"
                    f"Комментарий платежа: <b>order:{order.to_user_id}:{order.id}</b>\n\n"
                    f"⏳Перевод надо совершить в течении {admin_settings.pay_wait_time} минут.",
                    parse_mode="html"
                )
                await bot.send_message(order.to_user_id, settings.PRIZM_WALLET_ADDRESS)
                await bot.send_message(order.to_user_id, f"order:{order.to_user_id}:{order.id}")
            else:
                from_user_wallet = await crud_wallet.get_by_user_id_currency(session, currency=order.to_currency,
                                                                             user_id=order.from_user_id)
                await bot.send_message(
                    order.to_user_id,
                    f"Переведите {order.rub_value} рублей на реквизиты {from_user_wallet.value} \n"
                    f"⏳Перевод надо совершить в течении {admin_settings.pay_wait_time} минут.",
                    reply_markup=sent_card_transfer(order.id)
                )
                await bot.send_message(
                    cb.from_user.id,
                    f"Ждите перевод {order.rub_value} рублей от пользователя"
                )

            order_request = await crud_order_request.get_by_id(session, id=order.order_request_id)
            if order_request.max_limit > order.prizm_value:
                order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
                order_request_update_data = OrderRequestUpdate(
                    max_limit=order_request.max_limit - order.prizm_value,
                    max_limit_rub=order_request.max_limit_rub - order.rub_value,
                    status=OrderRequest.IN_PROGRESS
                )
                await crud_order_request.update(session, db_obj=order_request,
                                                obj_in=order_request_update_data)

        else:
            order = await crud_order.update(session, db_obj=order, obj_in={"status": Order.CANCELED})
            user_db = await crud_user.lock_row(session, id=user_db.id)
            from_cb_userdb = await crud_user.update(session, db_obj=user_db,
                                                    obj_in={"cancel_order_count": user_db.cancel_order_count + 1})
            await bot.send_message(
                cb.from_user.id,
                "Отмена ордера, ваш рейтинг понижен" + get_start_text(from_cb_userdb.balance,
                                                                      from_cb_userdb.order_count,
                                                                      from_cb_userdb.cancel_order_count),
                reply_markup=get_menu_kb(is_admin=from_cb_userdb.role == User.ADMIN_ROLE)
            )
            to_user_db = await crud_user.get_by_id(session, id=order.to_user_id)
            await bot.send_message(
                order.to_user_id,
                f"Отмена ордера №{order.id}\n" + get_start_text(to_user_db.balance, to_user_db.order_count,
                                                                to_user_db.cancel_order_count),
                reply_markup=get_menu_kb(is_admin=to_user_db.role == User.ADMIN_ROLE)
            )
            order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
            await crud_order_request.update(session, db_obj=order_request,
                                            obj_in={"status": OrderRequest.IN_PROGRESS})
            await cb.message.edit_reply_markup(reply_markup=None)
            return
        await crud_order.update(session, db_obj=order, obj_in={"status": Order.ACCEPTED})
