from sqlalchemy import Column, String, DateTime, BigInteger, func, Numeric, SmallInteger

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Settings(Base, ModelBase):
    id = Column(BigInteger, primary_key=True)
    order_wait_minutes = Column(BigInteger)
    pay_wait_time = Column(BigInteger)
    commission_percent = Column(BigInteger)
