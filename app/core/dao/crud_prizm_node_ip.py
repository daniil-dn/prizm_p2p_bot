from logging import getLogger
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import PrizmNodeIp
from app.core import dto
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CRUDPrizmNodeIp(CRUDBase[PrizmNodeIp, dto.PrizmNodeIPCreate, dto.PrizmNodeIPUpdate]):
    async def get_active(self, db: AsyncSession) -> Optional[PrizmNodeIp]:
        q = select(PrizmNodeIp).filter(PrizmNodeIp.is_active == True).order_by(PrizmNodeIp.is_priority.desc())
        res = await db.execute(q)
        logger.debug(
            f"PrizmNodeIp get active"
        )
        return res.scalar()


crud_prizm_node_ip = CRUDPrizmNodeIp(PrizmNodeIp)
