from sqlalchemy import (Column,
                        DateTime,
                        BigInteger,
                        func,
                        ForeignKey,
                        Index,
                        String,
                        SmallInteger,
                        Numeric)
from sqlalchemy.orm import relationship, Mapped
from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class OrderRequest(Base, ModelBase):
    __table_args__ = (
        Index('ix_from_to_currency_count', "from_currency", "to_currency", 'min_limit', "max_limit"),
    )
    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    user: Mapped["User"] = relationship(
        "User",
        backref="user_wallet",
        foreign_keys=[user_id])

    from_currency = Column(ForeignKey('currency.id'), nullable=False)
    to_currency = Column(ForeignKey('currency.id'), nullable=False)

    min_limit = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    max_limit = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    rate = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    status = Column(SmallInteger, nullable=False)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
