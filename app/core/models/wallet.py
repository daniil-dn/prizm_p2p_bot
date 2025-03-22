from sqlalchemy import (Column,
                        BigInteger,
                        func,
                        ForeignKey,
                        String, Index)
from sqlalchemy.orm import relationship, Mapped
from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class Wallet(Base, ModelBase):
    __tableargs__ = (
        Index('ix_user_order', "user_id", "order_id"),
        Index('ix_user_order', "user_id", "order_request_id"),
    )
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), index=True, nullable=False)
    order_id = Column(BigInteger, ForeignKey('order.id'), index=True, nullable=True)
    order_request_id = Column(BigInteger, ForeignKey('order_request.id'), index=True, nullable=True)
    user: Mapped["User"] = relationship(
        "User",
        backref="user",
        foreign_keys=[user_id])

    currency = Column(String(5), nullable=False)

    value = Column(String)

    created_at = Column(index=True, default=func.now())
    updated_at = Column(onupdate=func.now())
