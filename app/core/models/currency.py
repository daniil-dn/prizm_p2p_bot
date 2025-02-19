from sqlalchemy import Column, DateTime, BigInteger, func, ForeignKey, Index, String, SmallInteger

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class Currency(Base, ModelBase):
    id = Column(String, primary_key=True)
