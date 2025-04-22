from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatChannel
from app.core import dto
from app.core.dao.base import CRUDBase, ModelType


class CRUDChatChannel(CRUDBase[ChatChannel, dto.ChatChannelCreate, None]):
    async def get_by_user_id(self, session: AsyncSession, user_id: int):
        query = select(ChatChannel).where(ChatChannel.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_all_active(
            self, db: AsyncSession
    ):
        q = select(ChatChannel).where(ChatChannel.is_stopped == False)
        res = await db.execute(q)
        return res.scalars().all()


    async def drop_every_day_data(self, sessionmaker):
        async with sessionmaker() as session:
            query = update(ChatChannel).values(current_count=0, last_post=None)
            await session.execute(query)
            await session.commit()

crud_chat_channel = CRUDChatChannel(ChatChannel)
