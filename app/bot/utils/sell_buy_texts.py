from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui.order_seller_accept import contact_to_user, sent_card_transfer, recieved_card_transfer
from app.core.config import settings
from app.core.dao import crud_order, crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import Order


async def get_sell_buy_text(order_id: int, user_id: int, session: AsyncSession, bot: Bot):
    order = await crud_order.get_by_id(session, id=order_id)
    admin_settings = await crud_settings.get_by_id(session, id=1)
    prizm_with_commission = order.prizm_value + order.prizm_value * order.commission_percent
    if order.mode == 'sell':
        if order.status == Order.ACCEPTED:
            if user_id == order.from_user_id:
                await bot.send_message(
                    user_id,
                    f"Вы подтвердили сделку. Ждем когда продавец переведет криптовалюту в Бота",
                    reply_markup=contact_to_user(order.to_user_id, order)
                )
            else:
                await bot.send_message(
                    user_id,
                    f"Сделка №{order.id} подтверждена.\n"
                    f"Переведите {prizm_with_commission} PZM c коммиссией сервиса {order.commission_percent * 100}%\n"
                    f"Без комментария платеж потеряется!\n"
                    f"На кошелек сервиса: <b><code>{settings.PRIZM_WALLET_ADDRESS}</code></b>\n"
                    f"Комментарий платежа: <b><code>order:{order.to_user_id}:{order.id}</code></b>\n\n"
                    f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.\n",
                    parse_mode="html",
                    reply_markup=contact_to_user(order.from_user_id, order)
                )
        if order.status == Order.IN_PROGRESS:
            ...
    else:
        if order.status == Order.ACCEPTED:
            from_user_wallet = await crud_wallet.get_by_user_id_currency(session, currency=order.to_currency,
                                                                         user_id=order.from_user_id)
            if user_id == Order.from_user_id:
                await bot.send_message(
                    user_id,
                    f"Ждите перевод {order.rub_value} рублей от покупателя",
                    reply_markup=contact_to_user(order.to_user_id, order)
                )
            else:
                await bot.send_message(
                    user_id,
                    f"Переведите {order.rub_value} рублей на реквизиты {from_user_wallet.value} \n"
                    f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.",
                    reply_markup=sent_card_transfer(order, order.from_user_id)
                )
        elif order.status == Order.WAIT_DONE_TRANSFER:
            if user_id == order.from_user_id:
                await bot.send_message(order.from_user_id,
                                       f"Сделка: №{order.id}. Проверьте перевод средств на карту и сумму. Общая сумма сделки {order.rub_value} рублей. ",
                                       reply_markup=recieved_card_transfer(order, order.to_user_id))
                await bot.send_message(user_id,
                                       "Ждите подтверждение от продавца",
                                       reply_markup=contact_to_user(order.from_user_id, order))
            else:
                await bot.send_message(order.to_user_id,
                                       f"Сделка: №{order.id}. Проверьте перевод средств на карту и сумму. Общая сумма сделки {order.rub_value} рублей. ",
                                       reply_markup=recieved_card_transfer(order, cb.from_user.id))
                await bot.send_message("Ждите подтверждение от покупателя",
                                       reply_markup=contact_to_user(order.to_user_id, order))
