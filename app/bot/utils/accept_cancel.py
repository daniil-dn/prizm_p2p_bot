from aiogram import Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import sent_card_transfer
from app.bot.ui.order_seller_accept import contact_to_user
from app.core.config import settings
from app.core.dao import crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import Order


async def send_notification_to_actings(order: Order, bot: Bot, cb: CallbackQuery, session: AsyncSession) -> None:
    admin_settings = await crud_settings.get_by_id(session, id=1)
    if order.mode == "sell":
        prizm_with_commission = order.prizm_value + order.prizm_value * order.commission_percent
        await bot.send_message(
            cb.from_user.id,
            f"Вы подтвердили сделку. Ждем когда продавец переведет криптовалюту в Бота",
            reply_markup=contact_to_user(order.to_user_id, order)
        )
        await bot.send_message(
            order.to_user_id,
            f"Сделка №{order.id} подтверждена.\n"
            f"Переведите {prizm_with_commission} PZM c коммиссией сервиса {order.commission_percent * 100}%\n"
            f"Без комментария платеж потеряется!\n"
            f"На кошелек сервиса: <b><blockquote>{settings.PRIZM_WALLET_ADDRESS}</blockquote></b>\n"
            f"Комментарий платежа: <b>order:{order.to_user_id}:{order.id}</b>\n\n"
            f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.\n"
            f"Адрес: <blockquote>settings.PRIZM_WALLET_ADDRESS</blockquote>",
            parse_mode="html",
            reply_markup=contact_to_user(order.from_user_id, order)
        )
        # await bot.send_message(order.to_user_id, settings.PRIZM_WALLET_ADDRESS)
        # await bot.send_message(order.to_user_id, f"order:{order.to_user_id}:{order.id}")

    else:
        from_user_wallet = await crud_wallet.get_by_user_id_currency(session, currency=order.to_currency,
                                                                     user_id=order.from_user_id)
        await bot.send_message(
            order.to_user_id,
            f"Переведите {order.rub_value} рублей на реквизиты {from_user_wallet.value} \n"
            f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.",
            reply_markup=sent_card_transfer(order, order.from_user_id)
        )
        await bot.send_message(
            cb.from_user.id,
            f"Ждите перевод {order.rub_value} рублей от покупателя",
            reply_markup=contact_to_user(order.to_user_id, order)
        )
