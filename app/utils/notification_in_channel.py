from datetime import datetime, timedelta

from pytz import timezone
from aiogram import Bot

from app.core.dao import crud_chat_channel


async def notification_shediuled(bot: Bot, session):
    async with session() as session:
        chats = await crud_chat_channel.get_all(session)
        best_order_to_buy = ...
        best_order_to_sell = ...

    text = ''

    now = datetime.now(tz=timezone('Europe/Moscow'))
    chats = [chat for chat in chats if
             chat.current_count > 0 and now > chat.last_post + timedelta(minutes=chat.interval)]

    for chat in chats:
        start_time_str, end_time_str = chat.interval_in_day.split("-")

        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        if not (start_time <= now.time() <= end_time):
            continue

        try:
            await bot.send_message(chat.id, text)
            ... # upd count and last post time in db
        except:
            pass