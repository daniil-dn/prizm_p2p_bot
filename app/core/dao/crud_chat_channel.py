from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatChannel
from app.core import dto
from app.core.dao.base import CRUDBase


class CRUDChatChannel(CRUDBase[ChatChannel, None, None]):
    pass


crud_chat_channel = CRUDChatChannel(ChatChannel)
