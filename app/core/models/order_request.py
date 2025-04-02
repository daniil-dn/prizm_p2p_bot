from sqlalchemy import (Column,
                        DateTime,
                        BigInteger,
                        func,
                        ForeignKey,
                        Index,
                        SmallInteger,
                        Numeric, String)
from sqlalchemy.orm import relationship, Mapped
from app.core.db.base_class import Base
from app.core.models.model_base import ModelBase
from app.core.models.user import User


class OrderRequest(Base, ModelBase):
    WAIT_PRIZM = 0
    IN_PROGRESS = 1
    LOCK = 3
    DELETED = 4
    STOPPED = 5

    WALLET_SBP = 1
    WALLET_PZM = 2
    WALLET_CARD = 3

    __table_args__ = (
        Index('ix_from_to_currency_count', "from_currency", "to_currency", 'min_limit', "max_limit"),
        Index('ix_from_to_currency_count', "from_currency", "to_currency", 'min_limit_rub', "max_limit_rub"),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True, nullable=False)
    user: Mapped["User"] = relationship(
        "User",
        backref="user_wallet",
        foreign_keys=[user_id])

    from_currency = Column(String(5), nullable=False)
    to_currency = Column(String(5), nullable=False)

    min_limit = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    max_limit = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    min_limit_rub = Column(Numeric(18, 4, asdecimal=False), nullable=False)
    max_limit_rub = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    rate = Column(Numeric(18, 4, asdecimal=False), nullable=False)

    status = Column(SmallInteger, nullable=False)

    wallet_type = Column(SmallInteger, nullable=True)

    created_at = Column(DateTime(timezone=True), index=True, default=func.now())
    updated_at = Column(DateTime(timezone=True), index=True, onupdate=func.now())
