from logging import getLogger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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


crud_user = CRUDUser(User)
