from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.base import AbstractDTO
from src.domain.models.base import Base

MT = TypeVar("MT", bound=Base)
CD = TypeVar("CD", bound=AbstractDTO)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: CD):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self):
        raise NotImplementedError


@dataclass
class BaseSQLAlchemyRepository(Generic[MT, CD], AbstractRepository):
    session: AsyncSession
    model: Type[MT]

    async def add(self, data: CD) -> MT:
        self.session.add(obj := self.model(**asdict(data)))
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get_list(self) -> Sequence[MT]:
        return (await self.session.scalars(select(self.model))).all()
