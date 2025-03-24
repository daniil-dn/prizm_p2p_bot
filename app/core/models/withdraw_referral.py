from sqlalchemy import BigInteger, Column, Integer, ForeignKey, func, DateTime, Double

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class WithdrawReferral(Base, ModelBase):
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), index=True, nullable=False)
    summ = Column(Double)
    created_at = Column(DateTime, default=func.now())