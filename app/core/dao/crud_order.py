from logging import getLogger
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.dao.base import CRUDBase
# app
from app.core.models import OrderRequest, Order
from app.core import dto

logger = getLogger(__name__)


class CRUDOrder(CRUDBase[Order, dto.OrderCreate, dto.OrderUpdate]):
    async def get_by_status(self,
                            db: AsyncSession,
                            statuses) -> List[OrderRequest] | int:
        filters = [Order.status.in_(statuses)]
        query = select(Order).options(joinedload(Order.to_user), joinedload(Order.from_user)).filter(*filters)

        res = await db.execute(query)
        return res.scalars().all()


crud_order = CRUDOrder(Order)
