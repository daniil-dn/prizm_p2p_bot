from aiogram import Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.services.message_manager import MessageManager
from app.bot.ui import sent_card_transfer
from app.bot.ui.order_seller_accept import contact_to_user, sended_pzm_transfer_button
from app.core.config import settings
from app.core.dao import crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import Order


async def send_notification_to_actings(order: Order, bot: Bot, cb: CallbackQuery,
                                       session: AsyncSession, message_manager: MessageManager) -> None:
    admin_settings = await crud_settings.get_by_id(session, id=1)
    if order.mode == "sell":
        prizm_with_commission = order.prizm_value + order.prizm_value * order.commission_percent

        message = await bot.send_message(
            cb.from_user.id,
            f"Вы подтвердили сделку. Ждем когда продавец переведет криптовалюту в Бота",
            reply_markup=contact_to_user(order.to_user_id, order)
        )
        await message_manager.set_message_and_keyboard(
            user_id=cb.from_user.id, order_id=order.id,
            text="Вы подтвердили сделку. Ждем когда продавец переведет криптовалюту в Бота",
            keyboard=contact_to_user(order.to_user_id, order),
            message_id=message.message_id)
        order_pzm_markup = contact_to_user(order.from_user_id, order)
        order_pzm_markup.inline_keyboard.append([sended_pzm_transfer_button(order.from_user_id, order)])
        message = await bot.send_message(
            order.to_user_id,
            f"Сделка №{order.id} подтверждена.\n"
            f"Переведите {prizm_with_commission:.3f} PZM c коммиссией сервиса {order.commission_percent * 100}%\n"
            f"Без комментария платеж потеряется!\n"
            f"На кошелек сервиса: <b><code>{settings.PRIZM_WALLET_ADDRESS}</code></b>\n"
            f"Комментарий платежа: <b><code>order:{order.to_user_id}:{order.id}</code></b>\n\n"
            f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.\n",
            parse_mode="html",
            reply_markup=order_pzm_markup
        )
        await bot.send_message(order.to_user_id, text=settings.PRIZM_WALLET_ADDRESS, parse_mode='html')
        await bot.send_message(order.to_user_id, text=f"order:{order.to_user_id}:{order.id}", parse_mode='html')

        await message_manager.set_message_and_keyboard(
            user_id=order.to_user_id, order_id=order.id,
            text=[f"Сделка №{order.id} подтверждена.\n"
                  f"Переведите {prizm_with_commission:.3f} PZM c коммиссией сервиса {order.commission_percent * 100}%\n"
                  f"Без комментария платеж потеряется!\n"
                  f"На кошелек сервиса: <b><code>{settings.PRIZM_WALLET_ADDRESS}</code></b>\n"
                  f"Комментарий платежа: <b><code>order:{order.to_user_id}:{order.id}</code></b>\n\n"
                  f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.\n",
                  settings.PRIZM_WALLET_ADDRESS,
                  f"order:{order.to_user_id}:{order.id}"],
            keyboard=order_pzm_markup,
            message_id=message.message_id)

    else:
        from_user_wallet = await crud_wallet.get_by_order_user_id(session, order_id=order.id,
                                                                     user_id=order.from_user_id)
        message = await bot.send_message(
            order.to_user_id,
            f"Переведите {order.rub_value:.2f} рублей на реквизиты <code>{from_user_wallet.value}</code> \n"
            f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.",
            reply_markup=sent_card_transfer(order, order.from_user_id), parse_mode="html"
        )
        await bot.send_message(order.to_user_id, text=from_user_wallet.value, parse_mode='html')

        await message_manager.set_message_and_keyboard(
            user_id=order.to_user_id, order_id=order.id,
            text=[f"Переведите {order.rub_value:.2f} рублей на реквизиты <code>{from_user_wallet.value}</code> \n"
                 f"⏳Перевод надо совершить в течение {admin_settings.pay_wait_time} минут.", from_user_wallet.value],
            keyboard=sent_card_transfer(order, order.from_user_id),
            message_id=message.message_id)

        message = await bot.send_message(
            cb.from_user.id,
            f"Ждите перевод {order.rub_value:.2f} рублей от покупателя",
            reply_markup=contact_to_user(order.to_user_id, order)
        )
        await message_manager.set_message_and_keyboard(
            user_id=cb.from_user.id, order_id=order.id,
            text=f"Ждите перевод {order.rub_value:.2f} рублей от покупателя",
            keyboard=contact_to_user(order.to_user_id, order),
            message_id=message.message_id)


async def send_cancel_notification_to_actings(order: Order, bot: Bot, cb: CallbackQuery,
                                       session: AsyncSession, message_manager: MessageManager) -> None:

    await bot.send_message(
        cb.from_user.id,
        f"Сделка №{order.id} отменена. ",
        reply_markup=contact_to_user(order.to_user_id, order)
    )

    await bot.send_message(
        order.to_user_id,
        f"Сделка №{order.id} отменена.\n Откройте другую сделку"
    )
