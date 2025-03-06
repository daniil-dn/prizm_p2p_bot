from logging import getLogger

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.ui import recieved_card_transfer, get_menu_kb
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order, crud_user
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import User, Order
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

router = Router()

logger = getLogger(__name__)


@router.callback_query(F.data.startswith('sent_card_transfer_'))
async def accept_order_payment_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                  session: AsyncSession) -> None:
    async with session:
        order = await crud_order.get_by_id(session, id=int(cb.data.split('_')[-1]))
        await crud_order.update(db=session, db_obj=order, obj_in={"status": Order.IN_PROGRESS})
    card_info_user_text = f"Проверьте перевод средств на карту. Ордер: №{order.id} "
    if order.mode == "buy":
        await bot.send_message(order.from_user_id, card_info_user_text, reply_markup=recieved_card_transfer(order.id))
        await cb.answer("Ждите подтверждение от продавца")
    else:
        await bot.send_message(order.to_user_id, card_info_user_text, reply_markup=recieved_card_transfer(order.id))
        await cb.answer("Ждите подтверждение от Покупателя")
    await cb.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('card_transfer_recieved_'))
async def accept_card_transfer_recieved_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                           session: AsyncSession) -> None:
    await cb.message.edit_reply_markup(reply_markup=None)
    main_account = settings.PRIZM_WALLET_ADDRESS
    main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS
    async with session:
        order = await crud_order.lock_row(session, id=int(cb.data.split('_')[-1]))
        if order.status != Order.IN_PROGRESS:
            try:
                await cb.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            finally:
                return
        buyer_id = order.from_user_id if order.mode == 'sell' else order.to_user_id
        seller_id = order.to_user_id if order.mode == 'sell' else order.from_user_id
        prizm_value = order.prizm_value
        seller = await crud_user.lock_row(session, id=seller_id)
        await crud_user.update(session, db_obj=seller,
                               obj_in={'balance': seller.balance - prizm_value, "order_count": seller.order_count + 1})
        order = await crud_order.update(session, db_obj=order, obj_in={'status': Order.WAIT_DONE_TRANSFER})
        logger.info(f"Сняли с баланса пользователя {seller.id} - {prizm_value}. Ордер ждет завершения")

    await cb.message.reply(
        "Вы подтвердили оплату. Сделка завершена.\n" + get_start_text(user_db.balance, user_db.order_count,
                                                                      user_db.cancel_order_count),
        reply_markup=get_menu_kb(is_admin=order.to_user.role == User.ADMIN_ROLE)),

    async with session:
        buyer = await crud_user.lock_row(session, id=buyer_id)
        buyer = await crud_user.update(session, db_obj=buyer,
                                       obj_in={"order_count": buyer.order_count + 1})
        buyer_wallet = await crud_wallet.get_by_user_id_currency(session, user_id=buyer_id, currency='PRIZM')

        prizm_fetcher = PrizmWalletFetcher(settings.PRIZM_API_URL)
        try:
            send_value = int(prizm_value * (1 - order.commission_percent) * 100)
            result = await prizm_fetcher.send_money(buyer_wallet.value, secret_phrase=main_secret_phrase,
                                                    amount_nqt=send_value, deadline=60)
            logger.info(
                f"Перевод средств Ордер №{order.id} адрес: {buyer_wallet.value}, сумма: {send_value} -> {result}")
        except Exception as err:
            logger.error(
                f"Ошибка при переводе средств по ордеру №{order.id} на кошелек  {buyer_wallet.value}. Error: {str(err)}")
            await bot.send_message(buyer_id,
                                   "Возникла ошибка при переводе PRIZM вам на кошелек. Свяжитесь с поддержкой \n 👉 https://t.me/Nikita_Kononenko")
        else:
            buyer_text = "Продавец подтвердил оплату. PRIZM переведены вам на кошелек"
            await bot.send_message(buyer_id, buyer_text + get_start_text(buyer.balance, buyer.order_count,
                                                                         buyer.cancel_order_count),
                                   reply_markup=get_menu_kb(is_admin=buyer.role == User.ADMIN_ROLE))

        await crud_order.update(session, db_obj=order, obj_in={'status': Order.DONE})
        logger.info(f"Order: №{order.id} Перевели {buyer_id} -> {buyer_wallet.value} - {prizm_value}. Ордер завершен")
