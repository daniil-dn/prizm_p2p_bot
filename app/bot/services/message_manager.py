import json

from aiogram.types import InlineKeyboardMarkup

from app.bot.services.redis import RedisService


class MessageManager:
    def __init__(self):
        self.redis = RedisService()

    async def set_message_and_keyboard(self, user_id: int, order_id: int, text: str | list[str],
                                       keyboard: InlineKeyboardMarkup, message_id: int):
        key = f'{user_id}-{order_id}'
        data = {'text': text,
                'keyboard': keyboard.model_dump(),
                'message_id': message_id}
        await self.redis.set_data(key, data)

    async def get_message_and_keyboard(self, user_id: int, order_id: int):
        key = f'{user_id}-{order_id}'
        data = await self.redis.get_data(key)
        data['keyboard'] = InlineKeyboardMarkup.model_validate(data['keyboard'])
        return data

    async def delete_message_and_keyboard(self, user_id: int, order_id: int):
        key = f'{user_id}-{order_id}'
        await self.redis.delete_data(key)