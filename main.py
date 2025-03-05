import asyncio
import sys

from logging import getLogger

from app.bot import Bot
from app.core.config import settings

from app.core.logs.utils import config_logging
from app.prizm_check_scheduler import Scheduler

config_logging()

logger = getLogger(__name__)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("No target specified")
    target = sys.argv[1]

    logger.info(f'Start: DEBUG is {settings.DEBUG}')

    if target == "bot":
        bot = Bot(settings.BOT_TOKEN)
        asyncio.run(bot.start_pooling())

    elif target == "prizm_check_scheduler":
        asyncio.run(Scheduler().start())
    else:
        logger.error("No target procceded")