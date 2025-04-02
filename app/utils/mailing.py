import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dao import crud_user
from app.core.models import User


async def mailing_to_users(text: str, users: list[User], bot: Bot):
    for user in users:
        try:
            await bot.send_message(user.id, text=text)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            await bot.send_message(user.id, text=text)
        except:
            pass
