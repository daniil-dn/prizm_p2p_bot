from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import admin_panel_commot_kb
from app.core.dao import crud_user, crud_order, crud_order_request
from app.core.models import User, Order, OrderRequest

router = Router()


@router.callback_query(F.data.startswith('admin_panel_menu'))
async def admin_panel_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User, session: AsyncSession) -> None:
    if user_db.role not in User.ALL_ADMINS:
        await bot.send_message(
            cb.from_user.id,
            f"Вы не админ!")
    await state.clear()
    user_count = await crud_user.get_all_count(session)
    order_count = await crud_order.get_by_status(session, statuses=[Order.CREATED, Order.ACCEPTED, Order.IN_PROGRESS, Order.WAIT_DONE_TRANSFER], only_count=True)
    _, order_request_buy_count = await crud_order_request.get_by_value_filter_pagination(session,
                                                                            filter_user_id=0,
                                                                            from_currency="RUB",
                                                                            status=OrderRequest.IN_PROGRESS,
                                                                            is_rub=False)
    _, order_request_sell_count = await crud_order_request.get_by_value_filter_pagination(session,
                                                                            filter_user_id=0,
                                                                            from_currency="PRIZM",
                                                                            status=OrderRequest.IN_PROGRESS,
                                                                            is_rub=False)

    await bot.send_message(cb.from_user.id, text=f"Админ Панель\n\n"
                                                 f"Статистика:\n"
                                                 f"Кол-во юзеров: {user_count}\n"
                                                 f"Кол-во сделок: {order_count}\n"
                                                 f"Кол-во ордеров на покупку: {order_request_buy_count}\n"
                                                 f"Кол-во ордеров на продажу: {order_request_sell_count}\n", reply_markup=admin_panel_commot_kb(is_main_admin=user_db.role == User.MAIN_ADMIN))
