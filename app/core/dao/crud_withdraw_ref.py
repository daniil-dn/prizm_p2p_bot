from logging import getLogger

# app
from app.core.models import WithdrawReferral
from app.core.dao.base import CRUDBase

logger = getLogger(__name__)


class CrudWithdrawRef(CRUDBase[WithdrawReferral, None, None]):
    pass


crud_withdraw_ref = CrudWithdrawRef(WithdrawReferral)