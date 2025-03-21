from logging import getLogger
from typing import List, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# app
from app.core.models import Wallet
from app.core import dto
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CRUDWallet(CRUDBase[Wallet, dto.WalletCreate, dto.OrderUpdate]):
    async def get_by_user_id_currency(self,
                                      db: AsyncSession,
                                      user_id: int, currency: str) -> List[Wallet] | int:
        query = select(Wallet).filter(Wallet.user_id == user_id, Wallet.currency == currency)

        res = await db.execute(query)
        return res.scalar()


crud_wallet = CRUDWallet(Wallet)
