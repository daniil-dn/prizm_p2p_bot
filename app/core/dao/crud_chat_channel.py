from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload
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


crud_chat_channel = CRUDChatChannel(ChatChannel)
