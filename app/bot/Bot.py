import aiogram
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import Dialog, setup_dialogs
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from app.bot.handlers import get_routers
from app.bot.middlewares import DbSessionMiddleware, ExistsUserMiddleware
from app.bot.ui import get_default_commands
from app.core.config import settings
from app.core.db.session import SessionLocal


class Bot:
    __slots__ = 'bot', 'token', 'dp'

    def __init__(self, token):
        self.token = token
        self.bot = aiogram.Bot(token)
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DEFAULT_DB,
                      password=settings.REDIS_PASSWORD)

        self.dp = aiogram.Dispatcher(storage=RedisStorage(redis=redis,  key_builder=DefaultKeyBuilder(with_destiny=True)),
)

    async def start_pooling(self):
        self.dp.include_routers(*get_routers())
        await self.bot.set_my_commands(get_default_commands())
        db_session_middleware = DbSessionMiddleware(
            session_pool=SessionLocal
        )
        exists_user_middleware = ExistsUserMiddleware(
            session_pool=SessionLocal
        )
        # message
        self.dp.message.middleware(db_session_middleware)
        self.dp.message.middleware(exists_user_middleware)

        # pool
        self.dp.poll_answer.middleware(db_session_middleware)
        self.dp.poll_answer.middleware(exists_user_middleware)

        # callback_query
        self.dp.callback_query.middleware(db_session_middleware)
        self.dp.callback_query.middleware(exists_user_middleware)

        setup_dialogs(self.dp)

        await self.dp.start_polling(self.bot)
