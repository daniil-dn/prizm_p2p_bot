from aiogram.types import Message

from app.utils.text_check import check_interval


async def interval_in_day_filter(message: Message):
    if check_interval(message.text):
        return True
    return False