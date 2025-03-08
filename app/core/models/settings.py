from sqlalchemy import Column, Numeric, Integer

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Settings(Base, ModelBase):
    id = Column(Integer, primary_key=True)
    order_wait_minutes = Column(Integer)
    pay_wait_time = Column(Integer)
    commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=False)
    prizm_rate_diff = Column(Numeric(18, 2, asdecimal=False), nullable=False)
