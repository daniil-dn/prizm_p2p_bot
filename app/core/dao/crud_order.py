from logging import getLogger
from typing import List

from sqlalchemy import select, or_, and_, func
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
                            statuses, only_count=False) -> List[Order] | int:
        filters = [Order.status.in_(statuses)]


        if only_count:
            query = select(Order.id).options(joinedload(Order.to_user), joinedload(Order.from_user)).filter(*filters)
            res = (await db.execute(func.count(query.scalar_subquery()))).scalar()
        else:
            query = select(Order).options(joinedload(Order.to_user), joinedload(Order.from_user)).filter(*filters)
            res = (await db.execute(query)).scalars().all()
        return res


    async def get_sell_orders(self,
                              db: AsyncSession,
                              user_id) -> List[Order] | int:
        filters = [or_(and_(Order.to_user_id == user_id, Order.status == Order.DONE, Order.mode == 'sell'),
                       and_(Order.from_user_id == user_id, Order.status == Order.DONE, Order.mode == 'buy'))]
        query = select(Order).filter(*filters)
        res = await db.execute(query)
        return res.scalars().all()


crud_order = CRUDOrder(Order)
