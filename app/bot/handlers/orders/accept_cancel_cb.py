from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.bot.utils.accept_cancel import send_notification_to_actings
from app.core.dao import crud_order, crud_user, crud_order_request
from app.core.dto import OrderRequestUpdate
from app.core.models import User, Order, OrderRequest

router = Router()


@router.callback_query(F.data.startswith('order_request_accept_'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession) -> None:
    async with session:
        order = await crud_order.lock_row(session, id=int(cb.data.split('_')[3]))
        if order.status != Order.CREATED:
            await cb.message.edit_reply_markup(reply_markup=None)
            return

        if cb.data.split('_')[2] == "accept":
            await send_notification_to_actings(order=order, bot=bot, cb=cb, session=session)

            order_request = await crud_order_request.get_by_id(session, id=order.order_request_id)
            await crud_order.update(session, db_obj=order, obj_in={"status": Order.ACCEPTED})

            if order_request.max_limit > order.prizm_value:
                order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
                order_request_update_data = OrderRequestUpdate(
                    max_limit=order_request.max_limit - order.prizm_value,
                    max_limit_rub=order_request.max_limit_rub - order.rub_value,
                    status=OrderRequest.IN_PROGRESS
                )
                await crud_order_request.update(session, db_obj=order_request,
                                                obj_in=order_request_update_data)
            await cb.message.delete()
            return


@router.callback_query(F.data.startswith('order_request_cancel_'))
async def accept_cancel_order_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                 session: AsyncSession) -> None:
    async with session:
        order = await crud_order.lock_row(session, id=int(cb.data.split('_')[3]))

        order = await crud_order.update(session, db_obj=order, obj_in={"status": Order.CANCELED})
        user_db = await crud_user.lock_row(session, id=user_db.id)
        from_cb_userdb = await crud_user.update(session, db_obj=user_db,
                                                obj_in={"cancel_order_count": user_db.cancel_order_count + 1})
        await bot.send_message(
            cb.from_user.id,
            "Отмена сделки, ваш рейтинг понижен\n\n" + get_start_text(from_cb_userdb.balance,
                                                                      from_cb_userdb.order_count,
                                                                      from_cb_userdb.cancel_order_count),
            reply_markup=get_menu_kb(is_admin=from_cb_userdb.role == User.ADMIN_ROLE)
        )
        to_user_db = await crud_user.get_by_id(session, id=order.to_user_id)
        await bot.send_message(
            order.to_user_id,
            f"Отмена сделки №{order.id}\n" + get_start_text(to_user_db.balance, to_user_db.order_count,
                                                            to_user_db.cancel_order_count),
            reply_markup=get_menu_kb(is_admin=to_user_db.role == User.ADMIN_ROLE)
        )
        order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
        await crud_order_request.update(session, db_obj=order_request,
                                        obj_in={"status": OrderRequest.IN_PROGRESS})
