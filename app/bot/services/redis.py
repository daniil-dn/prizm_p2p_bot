import json

from redis.asyncio.client import Redis

from app.core.config import settings


class RedisService:
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DEFAULT_DB,
                  password=settings.REDIS_PASSWORD)

    async def set_data(self, key: str, data: dict):
        await self.redis.set(key, json.dumps(data))

    async def get_data(self, key: str):
        data = await self.redis.get(key)
        if not data:
            return
        return json.loads(data)
    async def delete_data(self, key: str):
        await self.redis.delete(key)