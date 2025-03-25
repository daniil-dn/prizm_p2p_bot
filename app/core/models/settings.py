from sqlalchemy import Column, Numeric, Integer

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Settings(Base, ModelBase):
    id = Column(Integer, primary_key=True)
    order_wait_minutes = Column(Integer, default=20)
    pay_wait_time = Column(Integer, default=20)
    commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=False, default=0.2)
    withdrawal_commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=False, default=0.1)
    prizm_rate_diff = Column(Numeric(18, 2, asdecimal=False), nullable=False, default=0.1)
    partner_commission_percent = Column(Numeric(18, 2, asdecimal=False), nullable=True, default=0.1)
