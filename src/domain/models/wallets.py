from sqlalchemy.orm import Mapped, mapped_column

from domain.models.base import Base


class Wallet(Base):
    address: Mapped[str] = mapped_column(index=True)
    bandwidth: Mapped[float]
    energy: Mapped[float]
    trx_balance: Mapped[float]
