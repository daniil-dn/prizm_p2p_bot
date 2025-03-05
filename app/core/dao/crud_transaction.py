from logging import getLogger
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# app
from app.core.models import Wallet, Transaction
from app.core import dto
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CRUDTransaction(CRUDBase[Transaction, dto.TransactionCreate, dto.TransactionUpdate]):
    async def get_by_transaction_id(self, db: AsyncSession, *, txn_id: str) -> Optional[Transaction]:
        q = select(Transaction).filter(Transaction.transaction_id == txn_id)
        res = await db.execute(q)
        logger.debug(
            f"Transaction get_by_transaction_id args:{txn_id} {res}"
        )
        return res.scalar_one_or_none()


crud_transaction = CRUDTransaction(Transaction)
