import datetime

import aiogram
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.bot.handlers import get_routers
from app.bot.middlewares import DbSessionMiddleware, ExistsUserMiddleware
from app.bot.middlewares.update_online import UpdateOnline
from app.bot.services.message_manager import MessageManager
from app.bot.ui import get_default_commands
from app.core.config import settings
from app.core.dao import crud_chat_channel
from app.core.db.session import SessionLocal
from app.utils.schedule_funcs.check_prizm_node_ips import prizm_node_ip_check_sheduled
from app.utils.schedule_funcs.notification_in_channel import notification_sheduled


class Bot:
    __slots__ = 'bot', 'token', 'dp', 'message_manager', 'scheduler'

    def __init__(self, token):
        self.token = token
        self.bot = aiogram.Bot(token)
        self.scheduler = AsyncIOScheduler()
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DEFAULT_DB,
                      password=settings.REDIS_PASSWORD)

        self.message_manager = MessageManager()
        self.dp = aiogram.Dispatcher(storage=RedisStorage(redis=redis,
                                                          key_builder=DefaultKeyBuilder(with_destiny=True)))

    def _setup_middleware(self):
        db_session_middleware = DbSessionMiddleware(
            session_pool=SessionLocal
        )
        exists_user_middleware = ExistsUserMiddleware(
            session_pool=SessionLocal
        )
        update_online_middleware = UpdateOnline(
            session_pool=SessionLocal
        )

        # message
        self.dp.message.middleware(db_session_middleware)
        self.dp.message.middleware(exists_user_middleware)
        self.dp.message.middleware(update_online_middleware)

        # pool
        self.dp.poll_answer.middleware(db_session_middleware)
        self.dp.poll_answer.middleware(exists_user_middleware)
        self.dp.poll_answer.middleware(update_online_middleware)

        # callback_query
        self.dp.callback_query.middleware(db_session_middleware)
        self.dp.callback_query.middleware(exists_user_middleware)
        self.dp.callback_query.middleware(update_online_middleware)
        self.dp.callback_query.middleware(CallbackAnswerMiddleware())

    async def start_pooling(self):
        self.dp.include_routers(*get_routers())
        await self.bot.set_my_commands(get_default_commands())

        self._setup_middleware()

        self.scheduler.add_job(notification_sheduled, 'interval',
                               minutes=1,
                               kwargs={'bot': self.bot, 'session': SessionLocal})
        self.scheduler.add_job(prizm_node_ip_check_sheduled, 'interval',
                               minutes=5, next_run_time=datetime.datetime.now(),
                               kwargs={'session': SessionLocal})
        self.scheduler.add_job(crud_chat_channel.drop_every_day_data,
                               trigger=CronTrigger(hour=0, minute=0),
                               kwargs={'sessionmaker': SessionLocal})
        self.scheduler.start()

        setup_dialogs(self.dp)

        await self.dp.start_polling(self.bot, message_manager=self.message_manager, scheduler=self.scheduler)
