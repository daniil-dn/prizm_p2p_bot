from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager

from app.bot.handlers.buy_sell.state import BuyState
from app.core.dao import crud_order_request, crud_settings
from app.core.models import OrderRequest


async def get_orders_getter(dialog_manager: DialogManager, **kwargs):
    exact_value = dialog_manager.dialog_data['exact_value']
    if dialog_manager.start_data['mode'] == 'buy':
        is_rub = True
        from_currency = "PRIZM"
    else:
        is_rub = False
        from_currency = "RUB"
    current_page = await dialog_manager.find("ID_STUB_SCROLL").get_page()
    limit = 10
    offset = current_page * limit
    async with dialog_manager.middleware_data['session'] as session:
        result, count = await crud_order_request.get_by_value_filter_pagination(session,
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
        if dialog_manager.start_data['mode'] == 'buy':
            prizm_value = exact_value / order.rate
            rub_value = exact_value
            order_text = f'Ордер: №{order.id}\nКурс 1pzm - {order.rate}руб\nЛимит: {order.min_limit_rub} - {order.max_limit_rub}руб\nЧисло сделок:{order.user.order_count} Число отказов: {order.user.cancel_order_count}\n\n'
        else:
            prizm_value = exact_value
            rub_value = exact_value * order.rate
            order_text = f'Ордер : №{order.id}\nКурс 1pzm - {order.rate}руб\nЛимит: {order.min_limit} - {order.max_limit}PZM\nЧисло сделок:{order.user.order_count} Число отказов: {order.user.cancel_order_count}\n\n'

        all_orders_text += order_text
        order_button = f'№{order.id}'
        orders_list_text.append({'order_text': order_button, "id": order.id})
    pages = (count + 9) // limit
    return {"pages": pages, "current_page": current_page + 1,
            "orders": orders_list_text, "all_orders_text": all_orders_text, "mode": dialog_manager.start_data['mode']}


async def get_mode(dialog_manager: DialogManager, **kwargs):
    mode = dialog_manager.start_data['mode']
    if dialog_manager.dialog_data.get('card_method') == "sbp":
        mode = "sbp"
    return {"mode": mode}


async def get_order_accept_wait_time(dialog_manager: DialogManager, **kwargs):
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
    order_text = await get_accept_order_text(dialog_manager, **kwargs)
    return {"wait_time": admin_settings.order_wait_minutes, "text": order_text}


async def get_accept_order_text(dialog_manager: DialogManager, **kwargs) -> dict:
    order_request_id = dialog_manager.dialog_data['order_id']
    if not order_request_id:
        return {"text": ""}
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)
        order_request = await crud_order_request.get_by_id(session, id=int(order_request_id))
    if dialog_manager.start_data['mode'] == 'sell':
        prizm_value = dialog_manager.dialog_data['exact_value']
        value_commission = prizm_value * admin_settings.commission_percent
        rub_value = dialog_manager.dialog_data['exact_value'] * order_request.rate
        success_text = (f"Продажа PRIZM\n"
                        f"Сумма в PRIZM: {prizm_value}\n"
                        f"Рублей: {rub_value}\n"
                        f"Общая сумма оплаты PRIZM {prizm_value + value_commission}, включая комиссию сервиса {admin_settings.commission_percent * 100}%\n"
                        )
    else:
        prizm_value = dialog_manager.dialog_data['exact_value'] / order_request.rate
        rub_value = dialog_manager.dialog_data['exact_value']
        success_text = (f"Покупка PRIZM\n"
                        f"Сумма в рублях: {rub_value}\n"
                        f"Количество покупаемых монет: {prizm_value}\n"
                        f"Вы получите {prizm_value} PZM"
                        )

    return success_text
