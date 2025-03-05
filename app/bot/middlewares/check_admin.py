from aiogram import Bot
from functools import wraps

from app.core.models import User


def check_admin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        bot = kwargs['bot']
        user_db = kwargs['user_db']
        if user_db.role != User.ADMIN_ROLE:
            await bot.send_message(user_db.id, "У вас нет доступов")
        else:
            return await func(*args, **kwargs)

    return wrapper
