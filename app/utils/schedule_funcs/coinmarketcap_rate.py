from logging import getLogger

from app.bot.services.redis import RedisService
from app.core.config import settings
from app.utils.coinmarketcap import get_currency_rate

logger = getLogger(__name__)


async def get_coinmarketcap_rate():
    rate = await get_currency_rate("PZM", "RUB", settings.COINMARKETCAP_API_KEY)
    redis = RedisService()
    await redis.set_data(redis.get_rate_coinmarketcap_key("PZM", "RUB"), rate)
