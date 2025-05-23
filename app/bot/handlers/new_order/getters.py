from aiogram_dialog import DialogManager

from app.core.dao import crud_settings
from app.utils.coinmarketcap import get_rate_from_redis


async def get_mode(dialog_manager: DialogManager, **kwargs):
    mode = dialog_manager.start_data['mode']
    if dialog_manager.dialog_data.get('card_method') == "sbp":
        mode = "sbp"
    session = dialog_manager.middleware_data['session']
    admin_settings = await crud_settings.get_by_id(session, id=1)

    return {"mode": mode, "min_order_value": admin_settings.min_order_prizm_value}


async def get_prizm_rate(dialog_manager: DialogManager, **kwargs):
    rate = await get_rate_from_redis("PZM", "RUB")
    admin_settings = await crud_settings.get_by_id(dialog_manager.middleware_data['session'], id=1)

    return {"prizm_rate": str(rate)[:7], "prizm_rate_diff_percent": admin_settings.prizm_rate_diff * 100}
