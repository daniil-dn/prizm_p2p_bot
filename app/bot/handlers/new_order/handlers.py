from datetime import date
from decimal import Decimal
from logging import getLogger

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
from redis.utils import dict_merge

from app.bot.handlers.new_order.state import NewOrderState
from app.bot.handlers.common import start_cmd
from app.bot.ui import order_seller_accept_kb
from app.core.config import settings
from app.core.dao import crud_order_request, crud_order
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import OrderCreate, WalletCreate, OrderRequestCreate
from app.core.models import OrderRequest, Order
from app.utils.coinmarketcap import get_currency_rate, rate_difference

logger = getLogger(__name__)


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили создание ордера")
    await dialog_manager.done()
    await start_cmd(callback.message, callback.bot, dialog_manager.middleware_data['state'],
                    dialog_manager.middleware_data['user_db'])


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


async def on_from_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['from_value'] = text_widget.get_value()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_to_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['to_value'] = text_widget.get_value()

    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_rate_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['rate'] = user_rate = text_widget.get_value()
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    # todo admin
    if rate_difference(rate, user_rate, 20):
        await message.answer(f'Указанный курс отличается от биржевого на 20%. Текущий курс {rate}')
        return

    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=NewOrderState.sell_card_info, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        value_rate = dialog_manager.dialog_data['rate']
        min_limit_rub = dialog_manager.dialog_data['from_value'] * value_rate
        max_limit_rub = dialog_manager.dialog_data['to_value'] * value_rate
        async with dialog_manager.middleware_data['session'] as session:
            order_request = OrderRequestCreate(
                user_id=message.from_user.id,
                from_currency="RUB",
                to_currency="PRIZM",
                min_limit=dialog_manager.dialog_data['from_value'],
                max_limit=dialog_manager.dialog_data['to_value'],
                min_limit_rub=min_limit_rub,
                max_limit_rub=max_limit_rub,
                rate=dialog_manager.dialog_data['rate'],
                status=OrderRequest.IN_PROGRESS
            )
            await crud_order_request.create(session, obj_in=order_request)
            text = "Ваш ордер на покупку PRIZM создан и размещен на бирже"
            await message.bot.send_message(message.from_user.id, text=text)
            await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)


async def on_sell_card_info_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager,
                                     data):
    """Обработчик выбора количества гостей."""
    sell_card_info = text_widget.get_value()
    value_rate = dialog_manager.dialog_data['rate']
    min_limit_rub = dialog_manager.dialog_data['from_value'] * value_rate
    max_limit_rub = dialog_manager.dialog_data['to_value'] * value_rate
    async with dialog_manager.middleware_data['session'] as session:
        if dialog_manager.start_data['mode'] == 'sell':
            wallet_currency = 'RUB'
        else:
            wallet_currency = 'PRIZM'
        wallet = await crud_wallet.get_by_user_id_currency(session, currency=wallet_currency,
                                                           user_id=dialog_manager.middleware_data['user_db'].id)
        if not wallet:
            wallet = WalletCreate(user_id=message.from_user.id, currency=wallet_currency, value=sell_card_info)
            await crud_wallet.create(session, obj_in=wallet)
        elif wallet.value != sell_card_info:
            await crud_wallet.update(session, db_obj=wallet, obj_in={"value": sell_card_info})

        order_request = OrderRequestCreate(
            user_id=message.from_user.id,
            from_currency="PRIZM",
            to_currency="RUB",
            min_limit=dialog_manager.dialog_data['from_value'],
            max_limit=dialog_manager.dialog_data['to_value'],
            min_limit_rub=min_limit_rub,
            max_limit_rub=max_limit_rub,
            rate=dialog_manager.dialog_data['rate'],
            status=OrderRequest.WAIT_PRIZM
        )
        order_request = await crud_order_request.create(session, obj_in=order_request)

    text = (f"Переведите {dialog_manager.dialog_data['to_value']} PRIZM "
            f"на кошелек сервиса: \n{settings.PRIZM_WALLET_ADDRESS}\n "
            f"Комментарий платежа: request:{order_request.user_id}:{order_request.id}")
    await message.bot.send_message(message.from_user.id, text=text)
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
