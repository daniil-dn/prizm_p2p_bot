from logging import getLogger
from typing import Optional, List, Sequence

from sqlalchemy import or_, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

# app
from app.core.dao.base import CRUDBase
from app.core.models import OrderRequest
from app.core import dto

logger = getLogger(__name__)


class CRUDOrderRequest(CRUDBase[OrderRequest, dto.OrderRequestCreate, dto.OrderRequestUpdate]):
    async def get_by_filter_pagination(self,
                                       db: AsyncSession,
                                       filter_user_id,
                                       from_currency,
                                       min_limit,
                                       max_limit,
                                       status,
                                       limit,
                                       offset, is_rub: bool = False) -> List[OrderRequest] | int:
        if is_rub:
            filters = [OrderRequest.user_id != filter_user_id,
                       OrderRequest.from_currency == from_currency,
                       or_(
                           and_(OrderRequest.min_limit_rub >= min_limit,
                                OrderRequest.max_limit_rub <= max_limit
                                ),
                           and_(
                               OrderRequest.min_limit_rub <= min_limit,
                               OrderRequest.max_limit_rub >= max_limit,
                           ),
                           and_(
                               OrderRequest.min_limit_rub <= min_limit,
                               OrderRequest.max_limit_rub > min_limit,
                               OrderRequest.max_limit_rub <= max_limit,
                           ),
                           and_(
                               OrderRequest.min_limit_rub >= min_limit,
                               OrderRequest.min_limit_rub < max_limit,
                               OrderRequest.max_limit_rub >= max_limit,
                           )
                       ),
                       OrderRequest.status == status
                       ]
        else:
            filters = [OrderRequest.user_id != filter_user_id, OrderRequest.from_currency == from_currency,
                       or_(
                           and_(OrderRequest.min_limit >= min_limit,
                                OrderRequest.max_limit <= max_limit
                                ),
                           and_(
                               OrderRequest.min_limit <= min_limit,
                               OrderRequest.max_limit >= max_limit,
                           ),
                           and_(
                               OrderRequest.min_limit <= min_limit,
                               OrderRequest.max_limit > min_limit,
                               OrderRequest.max_limit <= max_limit,
                           ),
                           and_(
                               OrderRequest.min_limit >= min_limit,
                               OrderRequest.min_limit < max_limit,
                               OrderRequest.max_limit >= max_limit,
                           )
                       ),
                       OrderRequest.status == status
                       ]
        count_query = select(func.count(OrderRequest.id)).filter(*filters)
        query = select(OrderRequest).options(joinedload(OrderRequest.user)).filter(*filters)

        query = query.limit(limit).offset(offset)
        res = await db.execute(query)
        res_count = await db.execute(count_query)
        logger.debug(
            f"OrderRequest get_by_filter min_limit:{min_limit} max_limit:{max_limit} status:{status} {res}"
        )
        return res.scalars().all(), res_count.scalar()


crud_order_request = CRUDOrderRequest(OrderRequest)
