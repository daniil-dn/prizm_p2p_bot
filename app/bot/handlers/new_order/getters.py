from aiogram_dialog import DialogManager

from app.core.config import settings
from app.core.dao import crud_settings
from app.utils.coinmarketcap import get_currency_rate


async def get_mode(dialog_manager: DialogManager, **kwargs):
    mode = dialog_manager.start_data['mode']
    if dialog_manager.dialog_data.get('card_method') == "sbp":
        mode = "sbp"
    return {"mode": mode}


async def get_prizm_rate(dialog_manager: DialogManager, **kwargs):
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    admin_settings = await crud_settings.get_by_id(dialog_manager.middleware_data['session'], id=1)

    return {"prizm_rate": str(rate)[:7], "prizm_rate_diff_percent": admin_settings.prizm_rate_diff * 100}
