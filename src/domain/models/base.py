from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr

from src.domain.values import _created_at, uuid_pk


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    oid: Mapped[uuid_pk]
    created_at: Mapped[_created_at]
