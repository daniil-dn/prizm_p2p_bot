from logging import getLogger
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# app
from app.core.models import Settings
from app.core import dto
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CRUDSettings(CRUDBase[Settings, dto.SettingsCreate, dto.SettingsUpdate]):
    pass


crud_settings = CRUDSettings(Settings)
