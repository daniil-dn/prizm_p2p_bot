from logging import getLogger

from app.core.dao.base import CRUDBase
# app
from app.core.models import OrderRequest, User, Order
from app.core import dto

logger = getLogger(__name__)


class CRUDOrder(CRUDBase[Order, dto.OrderCreate, dto.OrderUpdate]):
    pass


crud_order = CRUDOrder(Order)
