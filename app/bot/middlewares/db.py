from logging import getLogger
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

logger = getLogger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        if type(event) is Message:
            logger.info(f"Message {event.text} from user {event.from_user.id}")
        elif type(event) is CallbackQuery:
            logger.info(f"CallbackQuery {event.data} from user {event.from_user.id}")
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
