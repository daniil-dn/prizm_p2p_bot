from logging import getLogger
from typing import Optional

from requests import session
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

# app
from app.core.models import User
from app.core import dto
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CRUDUser(CRUDBase[User, dto.UserCreate, dto.UserUpdate]):
    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        q = select(User).filter(User.username == username)
        res = await db.execute(q)
        logger.debug(
            f"Telegram User get_by_username args:{username} {res}"
        )
        return res.scalar_one_or_none()

    async def increase_balance(self, db: AsyncSession, *, id: int, summ: float):
        q = update(User).where(User.id == id).values(balance=User.balance + summ)
        await db.execute(q)
        await db.commit()

    async def decrease_balance(self, db: AsyncSession, *, id: int, summ: float):
        q = update(User).where(User.id == id).values(balance=User.balance - summ)
        await db.execute(q)
        await db.commit()

    async def increase_referral_balance(self, db: AsyncSession, *, id: int, summ: float):
        q = update(User).where(User.id == id).values(referral_balance=User.referral_balance + summ)
        await db.execute(q)
        await db.commit()

    async def decrease_referral_balance(self, db: AsyncSession, *, id: int, summ: float):
        q = update(User).where(User.id == id).values(referral_balance=User.referral_balance - summ)
        await db.execute(q)
        await db.commit()

    async def get_invites(self, db: AsyncSession, *, id: int):
        q = (select(User).where(User.partner_id == id)
             .options(joinedload(User.to_orders),
                      joinedload(User.from_orders)))
        res = await db.execute(q)
        return res.scalars().unique().all()

    async def get_main_admin(self, db: AsyncSession):
        q = select(User).where(User.role == User.MAIN_ADMIN)
        res = await db.execute(q)
        return res.scalar()


crud_user = CRUDUser(User)
