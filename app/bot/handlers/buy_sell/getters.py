import random

from aiogram_dialog import DialogManager


async def get_orders_getter(dialog_manager: DialogManager, **kwargs):
    """Получение списка столов с учетом выбранной вместимости."""
    # current_page = await dialog_manager.find("ID_STUB_SCROLL").get_page()
    text_slots = f'{random.randint(10, 10000)} 0.001р|100prizm. ✅ 100 ❌ 0'
    return {"pages": 10,
        "slots": [{'slot_text': text_slots, "id": random.randint(1, 20000)} for
                  _
                  in
                  range(10)]}
