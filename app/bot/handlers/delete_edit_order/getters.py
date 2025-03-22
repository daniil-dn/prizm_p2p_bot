from aiogram_dialog import DialogManager
from requests import session

from app.core.config import settings
from app.core.dao import crud_order_request, crud_settings
from app.core.models import OrderRequest
from app.utils.coinmarketcap import get_currency_rate


async def orders_getter(dialog_manager: DialogManager, **kwargs):
    session = dialog_manager.middleware_data['session']
    user = dialog_manager.middleware_data['user_db']

    order_requests = await crud_order_request.get_by_user_id(session, user_id=user.id) or []
    order_requests_text_list = []
    for order_request in order_requests:
        if order_request.from_currency == "PRIZM":
            mode = "Продажа"
        else:
            mode = "Покупка"
        order_request_text = (
            f"Ордер №{order_request.id}\n"
            f"{mode}\n"
            f"{order_request.min_limit}-{order_request.max_limit} призм"
            f"\n Курс {order_request.rate}")
        order_requests_text_list.append(order_request_text)

    return {
        'there': len(order_requests) != 0,
        'texts': order_requests_text_list,
        'orders': order_requests,
    }

async def order_getter(dialog_manager: DialogManager, **kwargs):
    order_id = int(dialog_manager.dialog_data.get('order_id'))
    session = dialog_manager.middleware_data['session']
    order_request = await crud_order_request.get_by_id(session, id=order_id)
    if order_request.from_currency == "PRIZM":
        mode = "Продажа"
    else:
        mode = "Покупка"
    text = (f"Ордер №{order_request.id}\n"
            f"{mode}\n"
            f"{order_request.min_limit}-{order_request.max_limit} призм"
            f"\n Курс {order_request.rate}"
            )
    return {
        'text': text,
        'stopped': order_request.status == OrderRequest.STOPPED,
        'active': order_request.status != OrderRequest.STOPPED,
    }


async def get_prizm_rate(dialog_manager: DialogManager, **kwargs):
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    async with dialog_manager.middleware_data['session'] as session:
        admin_settings = await crud_settings.get_by_id(session, id=1)

    return {"prizm_rate": str(rate)[:7], "prizm_rate_diff_percent": admin_settings.prizm_rate_diff * 100}