from datetime import date
from decimal import Decimal

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.buy_sell.state import BuyState
from app.bot.handlers.common import start_cmd
from app.bot.ui import order_seller_accept_kb
from app.core.dao import crud_order_request, crud_order, crud_settings
from app.core.dao.crud_wallet import crud_wallet
from app.core.dto import OrderCreate, WalletCreate
from app.core.models import OrderRequest, Order


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("Вы отменили поиск ордеров")
    await dialog_manager.done()
    await start_cmd(callback.message, callback.bot, dialog_manager.middleware_data['state'],
                    dialog_manager.middleware_data['user_db'])


async def on_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=BuyState.to_value, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.back(show_mode=ShowMode.DELETE_AND_SEND)


async def on_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['exact_value'] = text_widget.get_value()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_card_info_input(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    value = text_widget.get_value()
    dialog_manager.dialog_data['card_info'] = value
    user_db = dialog_manager.middleware_data['user_db']
    if dialog_manager.start_data['mode'] == 'sell':
        currency = 'RUB'
    else:
        currency = 'PRIZM'
    async with dialog_manager.middleware_data['session'] as session:
        wallet = await crud_wallet.get_by_user_id_currency(session, currency=currency,
                                                           user_id=dialog_manager.middleware_data['user_db'].id)
        if not wallet:
            wallet = WalletCreate(user_id=user_db.id, currency=currency, value=value)
            await crud_wallet.create(session, obj_in=wallet)
        elif wallet.value != value:
            await crud_wallet.update(session, db_obj=wallet, obj_in={"value": value})

    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def process_order_request_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['order_id'] = item_id
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_accept_order_request_input(cb: CallbackQuery, button, dialog_manager: DialogManager):
    input_value = dialog_manager.dialog_data['exact_value']

    async with dialog_manager.middleware_data['session'] as session:
        settings = await crud_settings.get_by_id(session, id=1)
        order_request = await crud_order_request.lock_row(session, id=dialog_manager.dialog_data['order_id'])
        if order_request.status in (OrderRequest.LOCK, OrderRequest.CLOSED):
            await cb.message.answer(f"Заявка №{order_request.id} заблокирован. Выберите другую заявку")
            await dialog_manager.switch_to(BuyState.orders_list, show_mode=ShowMode.DELETE_AND_SEND)
            return
        if not order_request.min_limit_rub <= input_value <= order_request.max_limit_rub:
            await cb.message.answer(
                f"Неверная сумма, введите еще раз от {order_request.min_limit_rub} до {order_request.max_limit_rub}")
            return

        await crud_order_request.update(session, db_obj=order_request, obj_in={'status': OrderRequest.LOCK})
        prizm_value = dialog_manager.dialog_data['exact_value']
        value_commission = prizm_value * settings.commission_percent
        rub_value = dialog_manager.dialog_data['exact_value'] / order_request.rate

        order = OrderCreate(
            from_user_id=order_request.user_id,
            to_user_id=dialog_manager.middleware_data['user_db'].id,
            from_currency=order_request.from_currency,
            to_currency=order_request.to_currency,
            prizm_value=prizm_value,
            rub_value=rub_value,
            commission_percent=Decimal(settings.commission_percent),
            status=Order.CREATED,
            mode=dialog_manager.start_data['mode'],
            order_request_id=order_request.id
        )
        order = await crud_order.create(session, obj_in=order)

        if dialog_manager.start_data['mode'] == 'sell':
            success_text = f"Заявка №{order.id}. Продажа PRIZM\nСумма в prizm: {prizm_value}\nРублей: {rub_value}\n Общая сумма оплаты PRIZM {prizm_value}. Ждите подтверждения покупателя"
            seller_text = f"Новая заявка №{order.id} на покупку PRIZM\nСумма в рублях: {rub_value}\nКоличество покупаемых монет: {prizm_value}\nВы получите {prizm_value - value_commission} призм. Комиссия сервиса {settings.commission_percent * 100}%.\nКурс в ордере {order_request.rate}"
        else:
            success_text = f"Заявка №{order.id}. Покупка PRIZM\nСумма в рублях: {rub_value}\nКоличество покупаемых монет: {prizm_value}\nВы получите {prizm_value - value_commission} призм \nКомиссия сервиса {settings.commission_percent * 100}%.\n Общая сумма оплаты PRIZM {prizm_value} (с комиссией сервиса). Ждите подтверждения продавца"
            seller_text = f"Новая заявка №{order.id} на продажу PRIZM\nСумма в рублях: {from_value}\n Количество покупаемых монет: {prizm_value}\nКурс в ордере {order_request.rate}"
        await cb.message.answer(success_text)
        await cb.message.bot.send_message(order_request.user_id, seller_text,
                                          reply_markup=order_seller_accept_kb(order.id))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
