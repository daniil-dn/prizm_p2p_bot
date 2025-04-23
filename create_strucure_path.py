import asyncio
from logging import getLogger

from app.core.config import settings
from app.core.dao import crud_user


from app.core.db.session import SessionLocal
from app.core.logs.utils import config_logging

config_logging()
logger = getLogger(__name__)

async def create_structure():
    async with SessionLocal() as session:
        users = await crud_user.get_all(session)
        for user in users:
            logger.info(f"User id: {user.id} structure_path: {user.structure_path} partner_id: {user.partner_id}")
            if not user.structure_path:
                await crud_user.update_structure(session, user, user.partner_id)


if __name__ == '__main__':
    asyncio.run(create_structure())