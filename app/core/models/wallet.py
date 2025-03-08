from sqlalchemy import (Column,
                        DateTime,
                        BigInteger,
                        func,
                        ForeignKey,
                        String)
from sqlalchemy.orm import relationship, Mapped
from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class Wallet(Base, ModelBase):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    user: Mapped["User"] = relationship(
        "User",
        backref="user",
        foreign_keys=[user_id])

    currency = Column(ForeignKey('currency.id'), nullable=False)

    value = Column(String)

    created_at = Column(index=True, default=func.now())
    updated_at = Column(onupdate=func.now())
