import asyncio
from decimal import Decimal
from logging import getLogger

from aiogram import Bot

from app.bot.handlers.orders import accept_order_payment_cb
from app.bot.handlers.orders.accept_order_payment import accept_card_transfer_recieved_cb
from app.bot.ui import sent_card_transfer, recieved_card_transfer
from app.core.config import settings
from app.core.dao import crud_transaction, crud_order, crud_order_request, crud_user
from app.core.dao.crud_wallet import crud_wallet
from app.core.db.session import SessionLocal
from app.core.dto import TransactionCreate
from app.core.models import Order, OrderRequest
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

logger = getLogger(__name__)


class Scheduler():
    async def start(self):
        while True:
            await self.check_prizm_wallet()
            await asyncio.sleep(30)

    async def check_prizm_wallet(self):
        prizm_fetcher = PrizmWalletFetcher(settings.PRIZM_API_URL)
        main_account = settings.PRIZM_WALLET_ADDRESS
        main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS
        transactions_data = await prizm_fetcher.get_blockchain_transactions(main_account)
        transactions = transactions_data['transactions']
        bot = Bot(settings.BOT_TOKEN)
        async with SessionLocal() as session:
            for transaction in transactions:
                if transaction['recipientRS'] != main_account or transaction['confirmations'] <= 2:
                    logger.info(f"Транзакция {transaction['transaction']} исходящая. Без проверок")
                    continue
                exist_transaction = await crud_transaction.get_by_transaction_id(db=session,
                                                                                 txn_id=str(transaction['transaction']))
                if not exist_transaction:
                    logger.info(f"Новая транзакция: {transaction['transaction']}. Записываем в БД.")
                    decrypted_message_data = await prizm_fetcher.read_message(main_secret_phrase,
                                                                              transaction['transaction'])
                    decrypted_message = decrypted_message_data['decryptedMessage'] if decrypted_message_data.get(
                        "errorCode") is None else None
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
                    exist_transaction = await crud_transaction.create(session, obj_in=transaction_data)
                    logger.info(f"Транзакция {transaction['transaction']} записана в БД.")

                    if txn_type and txn_type == "order":
                        order = await crud_order.get_by_id(db=session, id=int(from_message_order_id))
                        transfer_user_id = order.to_user_id
                        user = await crud_user.lock_row(db=session, id=transfer_user_id)
                        user_balance = user.balance + exist_transaction.value
                        await crud_user.update(db=session, db_obj=user, obj_in={"balance": user_balance})

                        if order and order.mode == "sell" and order.status != Order.IN_PROGRESS:
                            if user_balance >= order.to_value:
                                await crud_order.update(db=session, db_obj=order, obj_in={"status": Order.IN_PROGRESS})
                                await bot.send_message(transfer_user_id,
                                                       f"Вы перевели PRIZM в бота. Ждите перевода на карту")
                                buyer_wallet = await crud_wallet.get_by_user_id_currency(db=session,
                                                                                         user_id=order.from_user_id,
                                                                                         currency=order.from_currency)
                                await bot.send_message(order.from_user_id,
                                                       f"Продавец перевел PRIZM. Переведите {order.to_value} {order.from_currency} на карту: {buyer_wallet.value}",
                                                       reply_markup=sent_card_transfer(order.id))
                            else:
                                await bot.send_message(transfer_user_id,
                                                       f"Вы внесли недостаточное кол-во монет PRIZM {order.from_value}. Вы перевели {user_balance}")


                    elif txn_type and txn_type == "order_request":
                        order_request = await crud_order_request.get_by_id(db=session, id=int(from_message_order_id))
                        user = await crud_user.lock_row(db=session, id=order_request.user_id)
                        user_balance = user.balance + exist_transaction.value
                        await crud_user.update(db=session, db_obj=user, obj_in={"balance": user_balance})
                        user_balance_rub = order_request.max_limit * order_request.rate
                        order_request = await crud_order_request.update(db=session, db_obj=order_request,
                                                                        obj_in={"status": OrderRequest.IN_PROGRESS,
                                                                                "max_limit": min(user_balance,
                                                                                                 order_request.max_limit),
                                                                                "max_limit_rub": min(user_balance_rub,
                                                                                                     order_request.max_limit_rub)})
                        await bot.send_message(order_request.user_id,
                                               f"Ваш Ордер размещен. Лимит корректирован от суммы платежа. Текущий лимит от {order_request.min_limit} до {order_request.max_limit}")

                else:
                    logger.info(f"Транзакция {transaction['transaction']} уже существует в БД.")
                    logger.info(f"Следующая проверка через 30секунд")
                    break
