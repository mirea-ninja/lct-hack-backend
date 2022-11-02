from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Adjustment, Apartment, Query
from app.models import ApartmentCreate, QueryCreate, QueryCreateBaseApartment, QueryCreateUserApartments, QueryPatch


class QueryRepository:
    @staticmethod
    async def create(db: AsyncSession, user: UUID4, model: QueryCreate) -> Query:
        pass

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[Query]:
        res = await db.execute(select(Query).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> Query:
        res = await db.execute(select(Query).where(Query.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryCreate) -> Query:
        query = await QueryRepository.get(db, guid)

        if query is None:
            raise HTTPException(404, "Запрос не найден")

        await db.execute(update(Query).where(Query.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(query)

        return query

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, user: UUID4, model: QueryPatch) -> Query:
        query = await QueryRepository.get(db, guid)

        if query is None:
            raise HTTPException(404, "Запрос не найден")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Query).where(Query.guid == guid).values(**model.dict()))
        await db.commit()
        await db.refresh(query)

        return query

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(Query).where(Query.guid == guid))
        await db.commit()

    @staticmethod
    async def set_base(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analog: QueryCreateBaseApartment
    ) -> Apartment:
        pass

    @staticmethod
    async def get_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4) -> List[Apartment]:
        pass

    @staticmethod
    async def create_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, analogs: List[ApartmentCreate]) -> None:
        pass

    @staticmethod
    async def set_analogs(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analogs: QueryCreateUserApartments
    ) -> Adjustment:
        pass
