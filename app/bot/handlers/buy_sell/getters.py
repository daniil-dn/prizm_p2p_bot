from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager
from pytz import timezone

from app.bot.handlers.buy_sell.state import BuyState
from app.bot.utils.parce import parce_time
from app.core.dao import crud_order_request, crud_settings
from app.core.models import OrderRequest


async def get_orders_getter(dialog_manager: DialogManager, **kwargs):
    exact_value = dialog_manager.dialog_data.get('exact_value')
    if dialog_manager.start_data['is_all_mode'] is True:
        exact_value = None

    if dialog_manager.start_data['mode'] == 'buy':
        is_rub = True
        from_currency = "PRIZM"
    else:
        is_rub = False
        from_currency = "RUB"
    current_page = await dialog_manager.find("ID_STUB_SCROLL").get_page()
    limit = 5
    offset = current_page * limit
    result, count = await crud_order_request.get_by_value_filter_pagination(dialog_manager.middleware_data['session'],
                                                                            filter_user_id=
                                                                            dialog_manager.middleware_data[
                                                                                'user_db'].id,
                                                                            from_currency=from_currency,
                                                                            value=exact_value,
                                                                            status=OrderRequest.IN_PROGRESS,
                                                                            limit=limit, offset=offset,
                                                                            is_rub=is_rub)

    orders_list_text = []
    all_orders_text = ""
    for order in result:  # type: OrderRequest
        user = order.user
        wallet_text = ""
        if order.wallet_type == OrderRequest.WALLET_SBP:
            wallet_text = "Способ оплаты: 🏦СБП\n"
        elif order.wallet_type == OrderRequest.WALLET_CARD:
            wallet_text = "Способ оплаты: 💳Карта\n"
        time_text = parce_time(user.last_online)
        if dialog_manager.start_data['mode'] == 'buy':
            order_text = (f'Ордер: №{order.id}\nКурс 1pzm - {order.rate}руб\n'
                          f'Лимит: {order.min_limit_rub} - {order.max_limit_rub}руб\n'
                          f'{wallet_text}'
                          f'Число сделок:{order.user.order_count}\n'
                          f'Число отказов: {order.user.cancel_order_count}\n'
                          f'{time_text}\n\n')
        else:
            order_text = (f'Ордер : №{order.id}\nКурс 1pzm - {order.rate}руб\n'
                          f'Лимит: {order.min_limit} - {order.max_limit}PZM\n'
                          f'Число сделок:{order.user.order_count}\n'
                          f'Число отказов: {order.user.cancel_order_count}\n'
                          f'{time_text}\n\n')

        all_orders_text += order_text
        order_button = f'№{order.id}'
        orders_list_text.append({'order_text': order_button, "id": order.id})
    pages = (count + 9) // limit
    return {"pages": pages, "current_page": current_page + 1,
            "orders": orders_list_text, "all_orders_text": all_orders_text, "mode": dialog_manager.start_data['mode']}


async def get_mode(dialog_manager: DialogManager, **kwargs):
    mode = dialog_manager.start_data['mode']
    is_all_mode = dialog_manager.start_data['is_all_mode']
    show_back_on_wallet_value = dialog_manager.start_data.get('show_back_on_wallet_value', True)
    wallet_mode = dialog_manager.start_data['mode']
    if dialog_manager.dialog_data.get('card_method') == "sbp":
        wallet_mode = "sbp"
    return {"wallet_mode": wallet_mode, "mode": mode, "is_all_mode": is_all_mode, "show_back_on_wallet_value": show_back_on_wallet_value}


async def get_order_accept_wait_time(dialog_manager: DialogManager, **kwargs):
    admin_settings = await crud_settings.get_by_id(dialog_manager.middleware_data['session'], id=1)
    order_text = await get_accept_order_text(dialog_manager, **kwargs)
    return {"wait_time": admin_settings.order_wait_minutes, "text": order_text}


async def get_accept_order_text(dialog_manager: DialogManager, **kwargs) -> dict:
    order_request_id = dialog_manager.dialog_data['order_id']
    if not order_request_id:
        return {"text": ""}
    session = dialog_manager.middleware_data['session']
    admin_settings = await crud_settings.get_by_id(session, id=1)
    order_request = await crud_order_request.get_by_id(session, id=int(order_request_id))
    if dialog_manager.start_data['mode'] == 'sell':
        prizm_value = dialog_manager.dialog_data['exact_value']
        value_commission = prizm_value * admin_settings.commission_percent
        rub_value = dialog_manager.dialog_data['exact_value'] * order_request.rate
        success_text = (f"Продажа PZM\n"
                        f"Сумма в PZM: {prizm_value:.2f}\n"
                        f"Рублей: {rub_value:.2f}\n"
                        f"Общая сумма оплаты PZM {prizm_value + value_commission:.2f}, "
                        f"включая комиссию сервиса {admin_settings.commission_percent * 100:.1f}%\n"
                        )
    else:
        prizm_value = dialog_manager.dialog_data['exact_value'] / order_request.rate
        rub_value = dialog_manager.dialog_data['exact_value']
        success_text = (f"Покупка PZM\n"
                        f"Сумма в рублях: {rub_value:.2f}\n"
                        f"Количество покупаемых PZM: {prizm_value:.2f}\n"
                        f"Вы получите {prizm_value:.2f} PZM"
                        )

    return success_text
