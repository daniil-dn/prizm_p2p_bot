from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from app.core.models import MessageBetween
from app.core import dto
from app.core.dao.base import CRUDBase


class CRUDMessage(CRUDBase[MessageBetween, dto.MessageCreate, None]):
    async def get_all_by_order_id(self, session: AsyncSession, order_id):
        query = select(MessageBetween).where(MessageBetween.order_id == order_id).options(
            joinedload(MessageBetween.from_user), joinedload(MessageBetween.to_user))
        result = await session.execute(query)
        return result.scalars().all()


crud_message = CRUDMessage(MessageBetween)
