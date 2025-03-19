from app.core.models import MessageBetween
from app.core import dto
from app.core.dao.base import CRUDBase



class CRUDMessage(CRUDBase[MessageBetween, dto.MessageCreate, None]):
    pass


crud_message = CRUDMessage(MessageBetween)