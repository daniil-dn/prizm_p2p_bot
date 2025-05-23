from logging import getLogger
from typing import Optional

from requests import session
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy_utils import Ltree

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
        user = await crud_user.lock_row(db, id=id)
        logger.info(
            f"Increase_balance: User {user.id} balance: {user.balance} summ: {summ}")
        return await crud_user.update(db, db_obj=user, obj_in={"balance": user.balance + summ})

    async def decrease_balance(self, db: AsyncSession, *, id: int, summ: float):
        user = await crud_user.lock_row(db, id=id)
        logger.info(
            f"Decrease_balance: User {user.id} balance: {user.balance} summ: {summ}")
        return await crud_user.update(db, db_obj=user, obj_in={"balance": user.balance - summ})

    async def increase_referral_balance(self, db: AsyncSession, *, id: int, summ: float):
        user = await crud_user.lock_row(db, id=id)
        logger.info(
            f"Increase_referral_balance: User {user.id} referral_balance: {user.referral_balance} summ: {summ}")
        return await crud_user.update(db, db_obj=user, obj_in={"referral_balance": user.referral_balance + summ})

    async def decrease_referral_balance(self, db: AsyncSession, *, id: int, summ: float):
        user = await crud_user.lock_row(db, id=id)
        logger.info(
            f"Decrease_referral_balance: User {user.id} referral_balance: {user.referral_balance} summ: {summ}")
        return await crud_user.update(db, db_obj=user, obj_in={"referral_balance": user.referral_balance - summ})

    async def get_invites(self, db: AsyncSession, *, id: int):
        q = (select(User).where(User.partner_id == id))
        res = await db.execute(q)
        return res.scalars().unique().all()

    async def get_main_admins(self, db: AsyncSession):
        q = select(User).where(User.role == User.MAIN_ADMIN)
        res = await db.execute(q)
        return res.scalars().all()

    async def get_descendant_users(self, db: AsyncSession, user_db: User):
        q = select(User).filter(User.structure_path.descendant_of(user_db.structure_path)).filter(User.id != user_db.id)
        res = await db.execute(q)
        descendants = res.scalars().all()
        grouped_descendants = {}
        for desc in descendants:
            # Считаем уровень вложенности по количеству точек
            level = str(desc.structure_path).count('.') + 1
            if level not in grouped_descendants:
                grouped_descendants[level] = []
            grouped_descendants[level].append(desc)

        return grouped_descendants

    async def update_structure(self, db: AsyncSession, db_obj: User, partner_id: int | str):
        structure_path = Ltree(str(db_obj.id))
        if partner_id:
            logger.info(f"Crud update_structure user: {db_obj.id} partner id: {partner_id}")
            partner_db = await crud_user.get_by_id(db, id=int(partner_id))
            if partner_db:
                logger.info(f"Crud update_structure partner user: {db_obj.id} partner in db: {partner_db.id}")
                partner_structure_path = (await self.update_structure(db, partner_db,
                                                                      partner_db.partner_id)).structure_path if not partner_db.structure_path else partner_db.structure_path
                structure_path = partner_structure_path + structure_path

        logger.info(f"Crud update_structure user: {db_obj.id} new structure_path: {structure_path}")
        db_obj = await self.update(db, db_obj=db_obj, obj_in={"structure_path": structure_path})
        return db_obj


crud_user = CRUDUser(User)
