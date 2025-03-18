from sqlalchemy import Column, DateTime, BigInteger, func, ForeignKey, \
    Numeric, Enum

from sqlalchemy.orm import relationship, Mapped

from app.core.db.base_class import Base
from app.core.models.enums import Currency
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class Transfer(Base, ModelBase):
    id = Column(BigInteger, primary_key=True)
    from_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    from_user: Mapped["User"] = relationship(
        "User",
        backref="from_user",
        foreign_keys=[from_user_id])

    to_user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    to_user: Mapped["User"] = relationship(
        "User",
        backref="to_user",
        foreign_keys=[to_user_id])

    currency = Column(Enum(Currency), nullable=False)

    value = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
