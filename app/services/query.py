from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import QueryCreate, QueryGet, QueryPatch
from app.repositories import QueryRepository


class QueryService:
    @staticmethod
    async def create(db: AsyncSession, user: UUID4, model: QueryCreate) -> QueryGet:
        query = await QueryRepository.create(db, user, model)
        return QueryGet.from_orm(query)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[QueryGet]:
        queries = await QueryRepository.get_all(db, offset=offset, limit=limit)
        if queries is None:
            raise HTTPException(404, "Запросы не найдены")
        return [QueryGet.from_orm(u) for u in queries]

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
