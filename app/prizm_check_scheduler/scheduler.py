import asyncio
from datetime import datetime
from decimal import Decimal
from logging import getLogger

import pytz
from aiogram import Bot

from app.bot.services.message_manager import MessageManager
from app.bot.ui import sent_card_transfer, get_menu_kb
from app.bot.ui.order_seller_accept import contact_to_user
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_transaction, crud_order, crud_order_request, crud_user, crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.db.session import SessionLocal
from app.core.dto import TransactionCreate, OrderRequestUpdate
from app.core.models import Order, OrderRequest, User
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

logger = getLogger(__name__)


class Scheduler:
    async def start(self):
        while True:
            check_prizm_task = self.check_prizm_wallet
            scan_orders_task = self.scan_orders
            await asyncio.gather(check_prizm_task(), scan_orders_task())
            await asyncio.sleep(30)

    async def check_prizm_wallet(self):
        message_manager = MessageManager()
        async with SessionLocal() as session:
            prizm_fetcher = await PrizmWalletFetcher().init_with_active_node(session)
            main_account = settings.PRIZM_WALLET_ADDRESS
            main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS
            transactions_data = await prizm_fetcher.get_blockchain_transactions(main_account)
            transactions = transactions_data['transactions']
            async with Bot(settings.BOT_TOKEN) as bot:
                for transaction in transactions:
                    if transaction['recipientRS'] != main_account:
                        logger.info(f"Транзакция {transaction['transaction']} исходящая. Без проверок")
                        continue
                    elif transaction['confirmations'] <= 1:
                        logger.info(f"Транзакция {transaction['transaction']} мало подтверждений")
                        continue
                    exist_transaction = await crud_transaction.get_by_transaction_id(db=session,
                                                                                     txn_id=str(
                                                                                         transaction['transaction']))
                    if not exist_transaction:
                        logger.info(f"Новая транзакция: {transaction['transaction']}. Записываем в БД.")
                        try:
                            decrypted_message_data = await prizm_fetcher.read_message(main_secret_phrase,
                                                                                      transaction['transaction'])
                        except Exception as err:
                            logger.error(f"Read message error: {err}")
                            decrypted_message = None
                        else:
                            decrypted_message = decrypted_message_data.get(
                                'decryptedMessage') if decrypted_message_data.get(
                                "errorCode") is None else None
                        # decrypted_message = "order:6185258473:34" # todo remove
                        from_message_order_id = None
                        from_user_id = None
                        txn_type = None
                        if decrypted_message and ":" in decrypted_message:
                            try:
                                from_message_order_id = decrypted_message.split(":")[
                                    -1]
                                from_user_id = decrypted_message.split(":")[-2]
                            except Exception:
                                pass
                            else:
                                if decrypted_message.split(":")[0] == "order":
                                    txn_type = "order"

                                else:
                                    txn_type = "order_request"

                        transaction_data = TransactionCreate(
                            transaction_id=transaction['transaction'],
                            from_wallet_address=transaction['senderRS'],
                            to_wallet_address=transaction['recipientRS'],
                            value=Decimal(transaction['amountNQT']) / 100,
                            fee=Decimal(transaction['feeNQT']) / 100,
                            order_id=from_message_order_id if txn_type and txn_type == "order" else None,
                            order_request_id=from_message_order_id if txn_type and txn_type == "order_request" else None,
                            user_id=from_user_id,
                            message_text=decrypted_message,
                            extra_data=transaction,
                            type=txn_type
                        )
                        # transaction_data.value = Decimal(121.2) # todo remove
                        exist_transaction = await crud_transaction.create(session, obj_in=transaction_data)
                        logger.info(
                            f"Транзакция {transaction['transaction']} записана в БД с id: {exist_transaction.id}.")

                        if txn_type and txn_type == "order":
                            order = await crud_order.get_by_id(db=session, id=int(from_message_order_id))
                            if not order:
                                logger.error(
                                    f"Возникли проблемы с транзакцией {transaction.transaction_id}. Такого ордера не существует: {transaction.order_id}")
                                continue
                            transfer_user_id = order.to_user_id
                            user = await crud_user.lock_row(db=session, id=transfer_user_id)

                            user_balance = user.balance + exist_transaction.value
                            await crud_user.update(db=session, db_obj=user, obj_in={"balance": user_balance})
                            logger.info(
                                f"Средства по транзакции {exist_transaction.id} зачислены пользователю {user.id} баланс: {user.balance} ")
                            if order and order.mode == "sell" and order.status != Order.IN_PROGRESS:
                                order_value_commission = order.prizm_value + (
                                        order.prizm_value * order.commission_percent)
                                if user_balance >= order_value_commission:
                                    user = await crud_user.lock_row(db=session, id=transfer_user_id)
                                    upd_user_balance = user.balance - order_value_commission
                                    user = await crud_user.update(db=session, db_obj=user,
                                                                  obj_in={"balance": upd_user_balance})

                                    logger.info(
                                        f"Сделка {order.id} принята. баланс продавца {user.id}: {user.balance}. Нужно монет для ордера {order.prizm_value} баланс юзера{upd_user_balance} ")
                                    logger.info(
                                        f"Сделка {order.id} user_id: {order_request.user_id} new_max_limit: {prizm_max_limit} new_max_limit_rub: {rub_max_limit}")
                                    await crud_order.update(db=session, db_obj=order,
                                                            obj_in={"status": Order.IN_PROGRESS})

                                    message = await bot.send_message(transfer_user_id,
                                                                     f"Сделка №{order.id}. Вы перевели PRIZM в бота. Ждите перевода на карту",
                                                                     reply_markup=contact_to_user(order.from_user_id,
                                                                                                  order))
                                    await message_manager.set_message_and_keyboard(
                                        user_id=transfer_user_id,
                                        order_id=order.id,
                                        text=f"Сделка №{order.id}. Вы перевели PRIZM в бота. Ждите перевода на карту",
                                        keyboard=contact_to_user(order.from_user_id, order),
                                        message_id=message.message_id
                                    )

                                    buyer_wallet = await crud_wallet.get_by_user_id_currency(db=session,
                                                                                             user_id=order.to_user_id,
                                                                                             currency=order.from_currency)
                                    message = await bot.send_message(order.from_user_id,
                                                                     f"Продавец перевел(а) PRIZM. Переведите {order.rub_value:.2f} 'RUB' на карту: {buyer_wallet.value}",
                                                                     reply_markup=sent_card_transfer(order,
                                                                                                     order.to_user_id))
                                    await message_manager.set_message_and_keyboard(
                                        user_id=order.from_user_id,
                                        order_id=order.id,
                                        text=f"Продавец перевел(а) PRIZM. Переведите {order.rub_value:.2f} 'RUB' на карту: {buyer_wallet.value}",
                                        keyboard=sent_card_transfer(order, order.to_user_id),
                                        message_id=message.message_id
                                    )

                                    logger.info(
                                        f"Сделка {order.id}. Сообщения отправлены пользователям. Продавцу {transfer_user_id}. Покупателю {order.to_user_id} ")
                                else:
                                    logger.info(
                                        f"Сделка {order.id} не принята. Баланс продавца: {order_value_commission}. Нужно монет для ордера {order.prizm_value} ")

                                    await bot.send_message(transfer_user_id,
                                                           f"Вы внесли недостаточное кол-во монет PRIZM {order_value_commission}. Вы перевели {user_balance}")


                        elif txn_type and txn_type == "order_request":

                            order_request = await crud_order_request.get_by_id(db=session,
                                                                               id=int(from_message_order_id))
                            logger.info(
                                f"Ордер реквест {from_message_order_id}. В БД  {order_request.id}")
                            if order_request:
                                user = await crud_user.lock_row(db=session, id=order_request.user_id)
                                admin_settings = await crud_settings.get_by_id(session, id=1)
                                order_request_pzm_commission = order_request.max_limit * admin_settings.commission_percent
                                all_user_balance = user.balance + exist_transaction.value - order_request_pzm_commission

                                balance_ramain = all_user_balance - order_request.max_limit
                                if balance_ramain < 0:
                                    balance_ramain = 0
                                else:
                                    balance_ramain = balance_ramain
                                await crud_user.update(db=session, db_obj=user, obj_in={"balance": balance_ramain})

                                prizm_max_limit = min(all_user_balance, order_request.max_limit)
                                rub_max_limit = min(all_user_balance * order_request.rate,
                                                    order_request.max_limit * order_request.rate)
                                logger.info(
                                    f"Ордер реквест {order_request.id} user_id: {order_request.user_id} new_max_limit: {prizm_max_limit} new_max_limit_rub: {rub_max_limit} balance_ramain: {balance_ramain}")
                                order_request = await crud_order_request.update(db=session, db_obj=order_request,
                                                                                obj_in={
                                                                                    "status": OrderRequest.IN_PROGRESS,
                                                                                    "max_limit": prizm_max_limit,
                                                                                    "max_limit_rub": rub_max_limit})
                                if all_user_balance < order_request.max_limit:
                                    text = (
                                        f"Ваш Ордер №{order_request.id} на продажу PRIZM создан и размещен в боте.\nЛимит скорректирован от суммы платежа. \nТекущий лимит от {order_request.min_limit} до {order_request.max_limit} PZM\n\n"
                                        f"Курс 1pzm - {order_request.rate}руб\nЛимит: {order_request.min_limit_rub} - {order_request.max_limit_rub}руб\nЧисло сделок:{user.order_count} Число отказов: {user.cancel_order_count}\n\n")
                                else:
                                    text = (
                                        f"Ваш Ордер №{order_request.id} на продажу PRIZM создан и размещен в боте.\n\n"
                                        f"Курс 1pzm - {order_request.rate}руб\nЛимит: {order_request.min_limit_rub} - {order_request.max_limit_rub}руб\nЧисло сделок:{user.order_count} Число отказов: {user.cancel_order_count}\n\n")

                            else:
                                logger.error(
                                    f"Возникли проблемы с транзакцией {transaction.transaction_id}. Такого ордер request не существует: {transaction.order_id}. Error: {str(err)}")
                                text = "Возникли проблемы с транзакцией. Обратитесь в поддержку"
                            try:
                                await bot.send_message(order_request.user_id,
                                                       text + get_start_text(
                                                           user.balance, user.referral_balance, user.order_count,
                                                           user.cancel_order_count),
                                                       reply_markup=get_menu_kb(is_admin=user.role in User.ALL_ADMINS))
                                logger.info(
                                    f"Ордер реквест {order_request.id}. Сообщение продавцу {order_request.user_id} отправлено. ")
                            except Exception as err:
                                logger.error(
                                    f"OrderRequest {order_request.id} ошибки при отправке сообщния для {order_request.user_id}. Error: {str(err)}")
                                continue

                    else:
                        logger.info(f"Транзакция {transaction['transaction']} уже существует в БД.")
                        logger.info(f"Следующая проверка через 30секунд")
                        break

    async def scan_orders(self):
        async with Bot(settings.BOT_TOKEN) as bot:
            async with SessionLocal() as session:
                admin_settings = await crud_settings.get_by_id(session, id=1)
                check_orders = await crud_order.get_by_status(db=session,
                                                              statuses=[Order.CREATED, Order.ACCEPTED])
                for order in check_orders:  # type: Order
                    current_time = datetime.now(tz=pytz.UTC).replace(tzinfo=None)
                    order_updated_at: datetime = order.updated_at if order.status != Order.CREATED else order.created_at
                    if order_updated_at.tzinfo:
                        order_updated_at = order_updated_at.replace(tzinfo=None)
                    if order.status == Order.CREATED:
                        logger.info(
                            f" Обработка Ордер {order.id} CREATED. Последнее обновление {order_updated_at}")
                        if (current_time - order_updated_at).total_seconds() > admin_settings.order_wait_minutes * 60:
                            logger.info(
                                f"Время для ордера {order.id} вышло - {order_updated_at}. Настройка {admin_settings.order_wait_minutes} минут")
                            await bot.send_message(order.from_user_id,
                                                   f"Время ожидания ордера превышено. Ордер №{order.id} отменен.\n\n" +
                                                   get_start_text(order.from_user.balance, order.from_user.referral_balance, order.from_user.order_count,
                                                                  order.from_user.cancel_order_count),
                                                   reply_markup=get_menu_kb(
                                                       is_admin=order.from_user.role in User.ALL_ADMINS))
                            await bot.send_message(order.to_user_id,
                                                   f"Время ожидания ордера превышено. Ордер №{order.id} отменен.\n\n" +
                                                   get_start_text(order.to_user.balance, order.to_user.referral_balance, order.to_user.order_count,
                                                                  order.to_user.cancel_order_count),
                                                   reply_markup=get_menu_kb(
                                                       is_admin=order.to_user.role in User.ALL_ADMINS))
                            await crud_order.update(db=session, db_obj=order, obj_in={"status": Order.CANCELED})
                            logger.info(
                                f"Ордер {order.id} - {order_updated_at} отменен. Сообщения для продавца и покупателя отправлены.")
                            if order.order_request_id:
                                order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
                                order_request_update_data = OrderRequestUpdate(
                                    max_limit=order_request.max_limit + order.prizm_value,
                                    max_limit_rub=order_request.max_limit_rub + order.rub_value,
                                    status=OrderRequest.IN_PROGRESS
                                )
                                await crud_order_request.update(session, db_obj=order_request,
                                                                obj_in=order_request_update_data)
                                logger.info(
                                    f"Ордер ревест {order_request.id} (ордер {order.id}). Обновлен - был лимит {order_request.max_limit} -> {order_request.max_limit + order.prizm_value}")
                            logger.info(
                                f"Ордер {order.id} отменен. Время ожидания {admin_settings.order_wait_minutes}мин платежа превышено.")


                    elif order.status == Order.ACCEPTED:
                        logger.info(
                            f" Обработка Ордер {order.id} ACCEPTED. Последнее обновление {order_updated_at}")
                        if (current_time - order_updated_at).total_seconds() > admin_settings.pay_wait_time * 60:
                            await bot.send_message(order.from_user_id,
                                                   f"Время ожидания платежа превышено. Ордер №{order.id} отменен.\n\n" +
                                                   get_start_text(order.from_user.balance, order.from_user.referral_balance, order.from_user.order_count,
                                                                  order.from_user.cancel_order_count),
                                                   reply_markup=get_menu_kb(
                                                       is_admin=order.from_user.role in User.ALL_ADMINS))
                            await bot.send_message(order.to_user_id,
                                                   f"Время ожидания платежа превышено. Ордер №{order.id} отменен.\n\n" +
                                                   get_start_text(order.to_user.balance, order.to_user.referral_balance, order.to_user.order_count,
                                                                  order.to_user.cancel_order_count),
                                                   reply_markup=get_menu_kb(
                                                       is_admin=order.to_user.role in User.ALL_ADMINS))
                            await crud_order.update(db=session, db_obj=order, obj_in={"status": Order.CANCELED})
                            logger.info(
                                f" Ордер {order.id} отменен. Сообщения отправлены. Последнее обновление {order_updated_at}. Настройка {admin_settings.pay_wait_time}")
                            if order.order_request_id:
                                order_request = await crud_order_request.lock_row(session, id=order.order_request_id)
                                order_request_update_data = OrderRequestUpdate(
                                    max_limit=order_request.max_limit + order.prizm_value,
                                    max_limit_rub=order_request.max_limit_rub + order.rub_value,
                                    status=OrderRequest.IN_PROGRESS
                                )
                                await crud_order_request.update(session, db_obj=order_request,
                                                                obj_in=order_request_update_data)
                            logger.info(
                                f"Ордер {order.id} отменен. Время ожидания {admin_settings.pay_wait_time}мин платежа превышено.")

                    elif order.status == Order.IN_PROGRESS:
                        pass
                    elif order.status == Order.WAIT_DONE_TRANSFER:
                        pass
