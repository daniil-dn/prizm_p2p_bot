from sqlalchemy import Column, String, DateTime, BigInteger, func, Numeric, SmallInteger

from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase


class User(Base, ModelBase):
    PRIZM_USER_ID = -1

    USER_ROLE = 1
    ADMIN_ROLE = 2

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(SmallInteger, nullable=True, default=USER_ROLE)
    phone = Column(String, unique=True, nullable=True)
    balance = Column(Numeric(18, 4, asdecimal=False), default=0)
    order_count = Column(BigInteger, default=0)
    cancel_order_count = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
