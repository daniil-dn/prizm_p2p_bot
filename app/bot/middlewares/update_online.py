from datetime import datetime
from logging import getLogger
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from pytz import timezone
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.dao import crud_user

logger = getLogger(__name__)


class UpdateOnline(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        async with self.session_pool() as db:
            exist_user = await crud_user.get_by_id(db, id=user.id)
            if exist_user:
                now = datetime.now(tz=timezone('utc'))
                update_user_data = {"last_online": now}
                await crud_user.update(db, db_obj=exist_user, obj_in=update_user_data)
        return await handler(event, data)
