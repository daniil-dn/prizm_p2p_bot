from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import get_menu_kb
from app.core.dao import crud_order_request
from app.core.models import User

router = Router()


@router.callback_query(F.data.startswith('my_order_requests'))
async def my_order_requests_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                               session: AsyncSession) -> None:
    await state.clear()
    async with session:
        order_requests_text_list = []
        order_requests = await crud_order_request.get_by_user_id(session, user_id=user_db.id)
        for order_request in order_requests:
            if order_request.from_currency == "PRIZM":
                mode = "Продажа"
            else:
                mode = "Покупка"
            order_request_text = (f"Ордер №{order_request.id}\n{mode}\n1-108 призм\n Курс 0,08")
            order_requests_text_list.append(order_request_text)

        res = "\n\n".join(order_requests_text_list)

        await bot.send_message(
            cb.from_user.id,
            f"""
Ваши размещеннные ордера:\n\n{res}
            """, reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE)
        )
