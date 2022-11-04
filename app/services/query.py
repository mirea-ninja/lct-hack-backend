from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AdjustmentGet,
    ApartmentCreate,
    ApartmentGet,
    QueryCreate,
    QueryCreateBaseApartment,
    QueryCreateUserApartments,
    QueryGet,
    QueryPatch,
)
from app.repositories import QueryRepository


class QueryService:
    @staticmethod
    async def create(db: AsyncSession, model: QueryCreate) -> QueryGet:
        query = await QueryRepository.create(db, model)
        return QueryGet.from_orm(query)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[QueryGet]:
        queries = await QueryRepository.get_all(db, offset=offset, limit=limit)
        if queries is None:
            raise HTTPException(404, "Запросы не найдены")
        return [QueryGet.from_orm(q) for q in queries]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> QueryGet:
        query = await QueryRepository.get(db, guid)
        if query is None:
            raise HTTPException(404, "Запрос не найден")
        return QueryGet.from_orm(query)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryCreate) -> QueryGet:
        query = await QueryRepository.update(db, guid, user, model)
        if query is None:
            raise HTTPException(404, "Запрос не найден")
        return QueryGet.from_orm(query)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryPatch) -> QueryGet:
        query = await QueryRepository.patch(db, guid, user, model)
        if query is None:
            raise HTTPException(404, "Запрос не найден")
        return QueryGet.from_orm(query)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await QueryRepository.delete(db, guid)
        return Response(status_code=204)

    @staticmethod
    async def set_base(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analog: QueryCreateBaseApartment
    ) -> ApartmentGet:
        query = await QueryRepository.get(db, guid)

        if query is None:
            raise HTTPException(404, "Запрос не найден")

        sub_query = await QueryRepository.get_subquery(db, subguid)
        if sub_query is None:
            raise HTTPException(404, "Подзапрос не найден")

        apartment = await QueryRepository.set_base(db, guid, subguid, user, analog)
        return ApartmentGet.from_orm(apartment)

    @staticmethod
    async def get_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4) -> list[ApartmentGet]:
        apartments = await QueryRepository.get_analogs(db, guid, subguid)
        if apartments is None:
            raise HTTPException(404, "Запросы не найдены")
        return [ApartmentGet.from_orm(a) for a in apartments]

    @staticmethod
    async def create_analogs(
        db: AsyncSession, guid: UUID4, subguid: UUID4, analogs: list[ApartmentCreate]
    ) -> Response(status_code=204):
        await QueryRepository.create_analogs(db, guid, subguid, analogs)
        return Response(status_code=204)

    @staticmethod
    async def set_analogs(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analogs: QueryCreateUserApartments
    ) -> AdjustmentGet:
        adjustment = await QueryRepository.set_analogs(db, guid, subguid, user, analogs)
        if adjustment is None:
            raise HTTPException(404, "Запрос не найден")
        return AdjustmentGet.from_orm(adjustment)
