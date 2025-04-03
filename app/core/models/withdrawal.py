from sqlalchemy import BigInteger, Column, Integer, ForeignKey, func, DateTime, Numeric, String, SmallInteger

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Withdrawal(Base, ModelBase):
    IN_PROGRESS = 1
    DONE = 2
    FAILED = 3

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), index=True, nullable=False)
    amount = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    commission_percent = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    wallet = Column(String)
    status = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
