from sqlalchemy import Column, String, DateTime, BigInteger, func, Numeric, SmallInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship

from app.core.db.base_class import Base
from app.core.models import Order
from app.core.models.model_base import ModelBase


class User(Base, ModelBase):
    MAIN_ADMIN = 3
    USER_ROLE = 1
    ADMIN_ROLE = 2

    ALL_ADMINS = (ADMIN_ROLE, MAIN_ADMIN)

    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(SmallInteger, nullable=True, default=USER_ROLE)
    partner_id = Column(BigInteger, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    balance = Column(Numeric(18, 4, asdecimal=False), default=0)
    referral_balance = Column(Numeric(18, 4, asdecimal=False), default=0, server_default="0", nullable=False)
    order_count = Column(BigInteger, default=0)
    cancel_order_count = Column(BigInteger, default=0)
    last_online = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), index=True, onupdate=func.now())

    from_orders: Mapped[list['Order']] = relationship('Order', back_populates='from_user', foreign_keys=[Order.from_user_id])
    to_orders: Mapped[list['Order']] = relationship('Order', back_populates='to_user', foreign_keys=[Order.to_user_id])