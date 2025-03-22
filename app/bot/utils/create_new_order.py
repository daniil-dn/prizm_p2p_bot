from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.bot.ui import get_menu_kb
from app.bot.ui.texts import get_start_text
from app.core.config import settings
from app.core.dao import crud_settings, crud_order_request
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import WalletCreate, OrderRequestCreate
from app.core.models import OrderRequest, Settings, User


async def create_order_and_wallet(dialog_manager: DialogManager, user_id: int, sell_card_info: str):
    value_rate = dialog_manager.dialog_data['rate']
    min_limit_rub = dialog_manager.dialog_data['from_value'] * value_rate
    max_limit_rub = dialog_manager.dialog_data['to_value'] * value_rate
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
        if dialog_manager.start_data['mode'] == 'sell':
            from_currency = "PRIZM"
            to_currency = "RUB"
            wallet_currency = 'RUB'
            order_request_status = OrderRequest.WAIT_PRIZM
        else:
            from_currency = "RUB"
            to_currency = "PRIZM"
            wallet_currency = 'PRIZM'
            order_request_status = OrderRequest.IN_PROGRESS

        order_request = OrderRequestCreate(
            user_id=user_id,
            from_currency=from_currency,
            to_currency=to_currency,
            min_limit=dialog_manager.dialog_data['from_value'],
            max_limit=dialog_manager.dialog_data['to_value'],
            min_limit_rub=min_limit_rub,
            max_limit_rub=max_limit_rub,
            rate=dialog_manager.dialog_data['rate'],
            status=order_request_status
        )
        order_request = await crud_order_request.create(session, obj_in=order_request)

        wallet = await crud_wallet.get_by_order_request_user_id(session,
                                                                user_id=dialog_manager.middleware_data['user_db'].id,
                                                                order_request_id=order_request.id)
        if not wallet:
            wallet = WalletCreate(user_id=user_id, order_request_id=order_request.id, currency=wallet_currency,
                                  value=sell_card_info)
            await crud_wallet.create(session, obj_in=wallet)
        elif wallet.value != sell_card_info:
            await crud_wallet.update(session, db_obj=wallet, obj_in={"value": sell_card_info})

        return order_request, admin_settings


async def send_notification(dialog_manager: DialogManager, admin_settings: Settings, order_request: OrderRequest,
                            message: Message):
    user_db = dialog_manager.middleware_data['user_db']

    if dialog_manager.start_data['mode'] == 'sell':
        value_with_commission = dialog_manager.dialog_data['to_value'] + dialog_manager.dialog_data[
            'to_value'] * admin_settings.commission_percent
        text = (
            f"Переведите {value_with_commission} PZM c коммиссией сервиса {admin_settings.commission_percent * 100}%"
            f"\nБез комментария платеж потеряется!\n"
            f"На кошелек сервиса:\n<b>{settings.PRIZM_WALLET_ADDRESS}</b>\n"
            f"Комментарий платежа:\n<b>request:{order_request.user_id}:{order_request.id}</b>\n\n"
            f"⏳Перевод надо совершить в течении {admin_settings.pay_wait_time} минут.")
        await message.bot.send_message(message.from_user.id, text=text, parse_mode='html')
        await message.bot.send_message(message.from_user.id, settings.PRIZM_WALLET_ADDRESS)
        await message.bot.send_message(message.from_user.id, f"request:{order_request.user_id}:{order_request.id}")
    else:
        text = (f"Ваш ордер №{order_request.id} на покупку PRIZM создан и размещен на бирже\n"
                f"Ордер: №{order_request.id}\nКурс 1pzm - {order_request.rate}руб\nЛимит: {order_request.min_limit_rub} "
                f"- {order_request.max_limit_rub}руб\nЧисло сделок:{user_db.order_count} Число отказов: "
                f"{user_db.cancel_order_count}\n\n") + get_start_text(
            user_db.balance, user_db.order_count,
            user_db.cancel_order_count)

        await message.bot.send_message(message.from_user.id, text=text,
                                       reply_markup=get_menu_kb(is_admin=user_db.role == User.ADMIN_ROLE))
