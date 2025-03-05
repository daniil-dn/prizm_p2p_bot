from aiogram_dialog import DialogManager

from app.core.dao import crud_order_request


async def get_mode(dialog_manager: DialogManager, **kwargs):
    """Получение списка столов с учетом выбранной вместимости."""
    return {"mode": dialog_manager.start_data['mode']}
