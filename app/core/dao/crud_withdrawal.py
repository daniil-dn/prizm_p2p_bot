from logging import getLogger

from app.core import dto
# app
from app.core.models import Withdrawal
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CrudWithdrawal(CRUDBase[Withdrawal, dto.WithdrawalCreate, dto.WithdrawalUpdate]):
    pass


crud_withdrawal = CrudWithdrawal(Withdrawal)
