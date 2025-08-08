from logging import getLogger
from typing import List

from sqlalchemy import or_, func, and_, desc, asc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

# app
from app.core.dao.base import CRUDBase
from app.core.models import OrderRequest, User
from app.core import dto

logger = getLogger(__name__)


class CRUDOrderRequest(CRUDBase[OrderRequest, dto.OrderRequestCreate, dto.OrderRequestUpdate]):
    async def get_by_limits_filter_pagination(self,
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

    async def get_by_value_filter_pagination(self,
                                             db: AsyncSession,
                                             filter_user_id,
                                             from_currency,
                                             status,
                                             value = None,
                                             limit = None,
                                             offset = None, is_rub: bool = False) -> List[OrderRequest] | int:

        if is_rub:
            filters = [OrderRequest.user_id != filter_user_id,
                       OrderRequest.from_currency == from_currency,
                       OrderRequest.status == status
                       ]
            if value:
                filters.append(
                    and_(OrderRequest.min_limit_rub <= value,
                         OrderRequest.max_limit_rub >= value
                         )
                )
        else:
            filters = [OrderRequest.user_id != filter_user_id,
                       OrderRequest.from_currency == from_currency,
                       OrderRequest.status == status
                       ]
            if value:
                filters.append(
                    and_(OrderRequest.min_limit <= value,
                         OrderRequest.max_limit >= value
                         )
                )
        count_query = select(func.count(OrderRequest.id)).filter(*filters)

        query = select(OrderRequest).filter(*filters).options(joinedload(OrderRequest.user)).join(User,
                                                                                                  User.id == OrderRequest.user_id).order_by(
            # todo зачем
            User.order_count)
        if limit and offset:
            query = query.limit(limit).offset(offset)
        res = await db.execute(query)
        res_count = await db.execute(count_query)
        logger.debug(
            f"OrderRequest get_by_filter value:{value} status:{status} {res}"
        )
        return res.scalars().all(), res_count.scalar()

    async def get_by_status(self,
                            db: AsyncSession,
                            statuses, only_count=False) -> List[OrderRequest] | int:

        filters = [OrderRequest.status.in_(statuses)]
        query = select(OrderRequest).options(joinedload(OrderRequest.user)).filter(*filters)

        if only_count:
            res = (await db.execute(func.count(query))).scalar()
        else:
            res = (await db.execute(query)).scalars().all()
        return res

    async def get_by_user_id(self,
                             db: AsyncSession,
                             user_id) -> List[OrderRequest] | int:

        filters = [OrderRequest.user_id == user_id, OrderRequest.status != OrderRequest.DELETED]
        query = select(OrderRequest).filter(*filters)

        res = await db.execute(query)
        return res.scalars().all()

    async def get_best_sell(self,
                            db: AsyncSession) -> OrderRequest:
        query = select(OrderRequest).where(OrderRequest.status == OrderRequest.IN_PROGRESS,
                                           OrderRequest.from_currency == 'PRIZM').order_by(
            asc(OrderRequest.rate)).options(joinedload(OrderRequest.user))

        res = await db.execute(query)
        return res.scalar()


    async def get_best_buy(self,
                            db: AsyncSession) -> OrderRequest:
        query = select(OrderRequest).where(OrderRequest.status == OrderRequest.IN_PROGRESS,
                                           OrderRequest.from_currency == 'RUB').order_by(
            desc(OrderRequest.rate)).options(joinedload(OrderRequest.user))

        res = await db.execute(query)
        return res.scalar()


crud_order_request = CRUDOrderRequest(OrderRequest)
