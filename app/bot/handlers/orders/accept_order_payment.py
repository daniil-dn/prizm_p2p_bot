from logging import getLogger

from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.services.message_manager import MessageManager
from app.bot.ui import recieved_card_transfer, get_menu_kb
from app.bot.ui.order_seller_accept import contact_to_user
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_order, crud_user, crud_settings, crud_order_request
from app.core.dao.crud_wallet import crud_wallet
from app.core.models import User, Order, OrderRequest
from app.prizm_check_scheduler.prizm_fetcher import PrizmWalletFetcher

router = Router()

logger = getLogger(__name__)


@router.callback_query(F.data.startswith('sent_card_transfer_'))
async def accept_order_payment_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                  session: AsyncSession, message_manager: MessageManager) -> None:
    order = await crud_order.get_by_id(session, id=int(cb.data.split('_')[-1]))
    order = await crud_order.update(db=session, db_obj=order, obj_in={"status": Order.WAIT_DONE_TRANSFER})
    card_info_user_text = f"Сделка: №{order.id}. Проверьте перевод средств на карту и сумму. Общая сумма сделки {order.rub_value:.2f} рублей. "
    if order.mode == "buy":
        message = await bot.send_message(order.from_user_id, card_info_user_text,
                                         reply_markup=recieved_card_transfer(order, order.to_user_id))
        await message_manager.set_message_and_keyboard(
            user_id=order.from_user_id, order_id=order.id,
            text=card_info_user_text,
            keyboard=recieved_card_transfer(order, order.to_user_id),
            message_id=message.message_id
        )

        message = await cb.message.reply("Ждите подтверждение от продавца",
                                         reply_markup=contact_to_user(order.from_user_id, order))
        await message_manager.set_message_and_keyboard(
            user_id=cb.from_user.id, order_id=order.id,
            text="Ждите подтверждение от продавца",
            keyboard=contact_to_user(order.from_user_id, order),
            message_id=message.message_id
        )
    else:
        message = await bot.send_message(order.to_user_id, card_info_user_text,
                                         reply_markup=recieved_card_transfer(order, cb.from_user.id))
        await message_manager.set_message_and_keyboard(
            user_id=order.to_user_id, order_id=order.id,
            text=card_info_user_text,
            keyboard=recieved_card_transfer(order, cb.from_user.id),
            message_id=message.message_id
        )

        message = await cb.message.reply("Ждите подтверждение от покупателя",
                                         reply_markup=contact_to_user(order.to_user_id, order))
        await message_manager.set_message_and_keyboard(
            user_id=cb.from_user.id, order_id=order.id,
            text="Ждите подтверждение от покупателя",
            keyboard=contact_to_user(order.to_user_id, order),
            message_id=message.message_id
        )
    await cb.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data.startswith('card_transfer_recieved_'))
async def accept_card_transfer_recieved_cb(cb: CallbackQuery, bot: Bot, state: FSMContext, user_db: User,
                                           session: AsyncSession, message_manager: MessageManager) -> None:
    # TODO чертовщина со статусами
    main_secret_phrase = settings.PRIZM_WALLET_SECRET_ADDRESS
    payout_wallet = settings.PRIZM_WALLET_ADDRESS_PAYOUT
    order = await crud_order.lock_row(session, id=int(cb.data.split('_')[-1]))
    if order.status != Order.WAIT_DONE_TRANSFER:
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
    payout_value = prizm_value * order.commission_percent
    admin_settings = await crud_settings.get_by_id(session, id=1)

    await message_manager.delete_message_and_keyboard(buyer_id, order.id)
    await message_manager.delete_message_and_keyboard(seller_id, order.id)

    seller = await crud_user.update(session, db_obj=seller,
                                    obj_in={"order_count": seller.order_count + 1})
    order = await crud_order.update(session, db_obj=order, obj_in={'status': Order.WAIT_DONE_TRANSFER})

    await cb.message.reply(
        "Вы подтвердили оплату. Сделка завершена. 🎉🎉🎉 \n" + get_start_text(seller.balance, seller.order_count,
                                                                           seller.cancel_order_count)),

    partner_commission = 0
    if seller.partner_id:
        partner_commissions = [6, 3, 1]
        index = 0
        for partner_id in seller.structure_path[:-1]:
            if index <= 2:
                partner_commission_percent = partner_commissions[index]
                partner_commission = payout_value * partner_commission_percent
                await crud_user.increase_referral_balance(session, id=int(partner_id.path),
                                                      summ=round(
                                                          partner_commission, 2))
            else:
                break
            index += 1
    buyer = await crud_user.lock_row(session, id=buyer_id)
    buyer = await crud_user.update(session, db_obj=buyer,
                                   obj_in={"order_count": buyer.order_count + 1})
    buyer_wallet = await crud_wallet.get_by_order_user_id(session, user_id=buyer_id, order_id=order.id)

    prizm_fetcher = PrizmWalletFetcher(settings.PRIZM_API_URL)
    try:
        result = await prizm_fetcher.send_money(buyer_wallet.value, secret_phrase=main_secret_phrase,
                                                amount_nqt=int(prizm_value * 100), deadline=60)

        logger.info(
            f"Сделка №{order.id} Перевод покупателю. адрес: {buyer_wallet.value}, сумма: {prizm_value:.3f} -> {result}")

    except Exception as err:
        logger.error(
            f"Ошибка при переводе средств по Сделке №{order.id} на кошелек  {buyer_wallet.value}. Error: {str(err)}")
        await bot.send_message(buyer_id,
                               f"Сделка №{order.id}. Возникла ошибка при переводе PRIZM вам на кошелек. Свяжитесь с поддержкой \n👉 https://t.me/Nikita_Kononenko" + get_start_text(
                                   buyer.balance, buyer.order_count,
                                   buyer.cancel_order_count),
                               reply_markup=get_menu_kb(is_admin=buyer.role in User.ALL_ADMINS))
    else:
        buyer_text = "Продавец подтвердил оплату. PRIZM переведены вам на кошелек 🎉🎉🎉"
        await bot.send_message(buyer_id, buyer_text + get_start_text(buyer.balance, buyer.order_count,
                                                                     buyer.cancel_order_count),
                               reply_markup=get_menu_kb(is_admin=buyer.role in User.ALL_ADMINS))
    try:
        result_payout = await prizm_fetcher.send_money(payout_wallet, secret_phrase=main_secret_phrase,
                                                       amount_nqt=int((payout_value - partner_commission) * 100),
                                                       deadline=60)
        logger.info(
            f"Перевод прибыли Сделка №{order.id} адрес: {payout_wallet}, сумма: {payout_value - partner_commission}. \npayout: {result_payout}")
        if partner_commission > 0:
            result_commission = await prizm_fetcher.send_money(settings.PRIZM_WALLET_ADDRESS_PARTNER_COMMISSION,
                                                               secret_phrase=main_secret_phrase,
                                                               amount_nqt=int(partner_commission * 100),
                                                               deadline=60)
            logger.info(
                f"Перевод реф прибыли партнера Сделка №{order.id} Partner_id: {buyer.partner_id} адрес: {settings.PRIZM_WALLET_ADDRESS_PARTNER_COMMISSION} -> {result_commission}")


    except Exception as err:
        logger.error(
            f"Ошибка при переводе реф прибыли по Сделке №{order.id} на кошелек  {payout_wallet}. Error: {str(err)}")

    order_request = await crud_order_request.get_by_id(session, id=order.order_request_id)
    if order_request.status == OrderRequest.DELETED and order_request.max_limit == order_request.min_limit:
        await cb.message.reply(
            f'Остаток призм по вашему ордеру №{order_request.id} менее {admin_settings.min_order_prizm_value} PZM и составляет {order_request.max_limit} PZM. Ордер закрыт. Средства перечислены на ваш общий баланс в боте и будут использованы при создании нового ордера, либо выведены при снятии средств с баланса.')

    await crud_order.update(session, db_obj=order, obj_in={'status': Order.DONE})
    logger.info(f"Сделка: №{order.id} Перевели {buyer_id} -> {buyer_wallet.value} - {prizm_value}. Сделка завершена")
