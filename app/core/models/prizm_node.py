from sqlalchemy import Column, String, DateTime, BigInteger, func, Boolean
from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class PrizmNodeIp(Base, ModelBase):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=True)
    ip = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_priority = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())