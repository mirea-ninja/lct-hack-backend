from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from pydantic import UUID4, BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response

ModelBase = TypeVar("ModelBase", bound=BaseModel)
ModelCreate = TypeVar("ModelCreate", bound=BaseModel)
ModelPatch = TypeVar("ModelPatch", bound=BaseModel)


class BaseService(
    ABC,
    Generic[
        ModelBase,
        ModelCreate,
        ModelPatch
    ],
):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def create(self, db: AsyncSession, user: UUID4, model: ModelCreate) -> ModelBase:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelBase]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, db: AsyncSession, user: UUID4, id: UUID4) -> ModelBase:
        raise NotImplementedError

    @abstractmethod
    async def update(self, db: AsyncSession, user: UUID4, id: UUID4, model: ModelCreate) -> ModelBase:
        raise NotImplementedError

    @abstractmethod
    async def patch(self, db: AsyncSession, user: UUID4, id: UUID4, model: ModelPatch) -> ModelBase:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, db: AsyncSession, user: UUID4, id: UUID4) -> Response(status_code=204):
        raise NotImplementedError
