from datetime import date
from decimal import Decimal

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput

from app.bot.handlers.buy_sell.state import BuyState
from app.bot.handlers.common import start_cmd
from app.bot.ui import order_seller_accept_kb
from app.core.dao import crud_order_request, crud_order
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


async def on_from_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['from_value'] = text_widget.get_value()
    await dialog_manager.next(show_mode=ShowMode.DELETE_AND_SEND)


async def on_to_value_selected(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    """Обработчик выбора количества гостей."""
    dialog_manager.dialog_data['to_value'] = text_widget.get_value()

    if dialog_manager.start_data['mode'] == 'sell':
        await dialog_manager.switch_to(state=BuyState.orders_list, show_mode=ShowMode.DELETE_AND_SEND)
    else:
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


async def on_exactly_value_input(message: Message, text_widget: ManagedTextInput, dialog_manager: DialogManager, data):
    dialog_manager.dialog_data['value'] = text_widget.get_value()
    input_value = text_widget.get_value()
    # todo проверки на лимит

    async with dialog_manager.middleware_data['session'] as session:
        order_request = await crud_order_request.lock_row(session, id=dialog_manager.dialog_data['order_id'])
        if order_request.status in (OrderRequest.LOCK, OrderRequest.CLOSED):
            await message.answer("Ордер заблокирован. Выберите другой ордер")
            await dialog_manager.switch_to(BuyState.orders_list, show_mode=ShowMode.DELETE_AND_SEND)
            return
        if not order_request.min_limit_rub <= input_value <= order_request.max_limit_rub:
            await message.answer("Неверная сумма ордера, введите еще раз")
            return

        await crud_order_request.update(session, db_obj=order_request, obj_in={'status': OrderRequest.LOCK})
        if dialog_manager.start_data['mode'] == 'buy':
            from_value = dialog_manager.dialog_data['value']
            to_value = dialog_manager.dialog_data['value'] / order_request.rate
            value_commission = to_value * 0.10  # todo commission
        else:
            from_value = dialog_manager.dialog_data['value'] / order_request.rate
            to_value = dialog_manager.dialog_data['value']
            value_commission = from_value * 0.10

        order = OrderCreate(
            from_user_id=order_request.user_id,
            to_user_id=dialog_manager.middleware_data['user_db'].id,
            from_currency=order_request.from_currency,
            to_currency=order_request.to_currency,
            from_value=from_value,
            to_value=to_value,
            commission_percent=Decimal(0.10),
            status=Order.CREATED,
            mode=dialog_manager.start_data['mode'],
            order_request_id=order_request.id
        )
        order = await crud_order.create(session, obj_in=order)

        if dialog_manager.start_data['mode'] == 'sell':
            success_text = f"Заявка {order.id}. Продажа PRIZM\nСумма в prizm: {from_value}\nРублей: {to_value}\n Общая сумма оплаты PRIZM {from_value}. Ждите подтверждения покупателя"
            seller_text = f"Новая заявка {order.id} на покупку PRIZM\nСумма в рублях: {to_value}\nКоличество покупаемых монет: {from_value}\nВы получите {from_value - value_commission} призм. Комиссия сервиса 10%.\nКурс в ордере {order_request.rate}"
        else:
            # todo commission
            success_text = f"Заявка {order.id}. Покупка PRIZM\nСумма в рублях: {from_value}\nКоличество покупаемых монет: {to_value}\nВы получите {to_value - value_commission} призм \nКомиссия сервиса 10%.\n Общая сумма оплаты PRIZM {to_value} (с комиссией сервиса). Ждите подтверждения продавца"
            seller_text = f"Новая заявка {order.id} на продажу PRIZM\nСумма в рублях: {from_value}\n Количество покупаемых монет: {to_value}\nКурс в ордере {order_request.rate}"
        await message.answer(success_text)
        await message.bot.send_message(order_request.user_id, seller_text,
                                       reply_markup=order_seller_accept_kb(order.id))
    await dialog_manager.done(show_mode=ShowMode.DELETE_AND_SEND)
