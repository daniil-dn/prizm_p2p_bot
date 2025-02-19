from logging import getLogger
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.dao import crud_user
from app.core.dto.user import UserCreate, UserUpdate

logger = getLogger(__name__)


class ExistsUserMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        async with (self.session_pool() as db):
            exist_user = await crud_user.get_by_id(db, id=user.id)
            if not exist_user:
                logger.debug(f'Create user in DB {user.id} {user.username} {user.first_name} {user.last_name}')
                create_user_data = UserCreate(
                    id=user.id,
                    language_code=user.language_code,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                )
                exist_user = await crud_user.create(db, obj_in=create_user_data)
            elif exist_user.username != user.username \
                    or exist_user.first_name != user.first_name \
                    or exist_user.last_name != user.last_name:
                update_user_data = UserUpdate(
                    id=user.id,
                    language_code=user.language_code,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                )
                exist_user = await crud_user.update(db, db_obj=exist_user, obj_in=update_user_data)
            data['user_db'] = exist_user
        return await handler(event, data)
