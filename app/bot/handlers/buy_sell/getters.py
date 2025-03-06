from aiogram_dialog import DialogManager

from app.core.dao import crud_order_request
from app.core.models import OrderRequest


async def get_orders_getter(dialog_manager: DialogManager, **kwargs):
    """Получение списка столов с учетом выбранной вместимости."""
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
        result, count = await crud_order_request.get_by_filter_pagination(session,
                                                                          filter_user_id=dialog_manager.middleware_data[
                                                                              'user_db'].id,
                                                                          from_currency=from_currency,
                                                                          value=exact_value,
                                                                          status=OrderRequest.IN_PROGRESS,
                                                                          limit=limit, offset=offset, is_rub=is_rub)

    orders_list_text = []
    for order in result:
        if dialog_manager.start_data['mode'] == 'buy':
            prizm_value = exact_value / order.rate
            rub_value = exact_value
        else:
            prizm_value = exact_value
            rub_value = exact_value * order.rate
        order_text = f'№{order.id} {order.rate}р / {prizm_value} PRIZM {rub_value} RUB  ✅{order.user.order_count}  ❌{order.user.cancel_order_count}'
        orders_list_text.append({'order_text': order_text, "id": order.id})
    pages = (count + 9) // limit
    return {"pages": pages, "current_page": current_page + 1,
            "orders": orders_list_text}


async def get_mode(dialog_manager: DialogManager, **kwargs):
    """Получение списка столов с учетом выбранной вместимости."""
    return {"mode": dialog_manager.start_data['mode']}
