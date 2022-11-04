from typing import List

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Adjustment, Apartment, Query, SubQuery
from app.models import ApartmentCreate, QueryCreate, QueryCreateBaseApartment, QueryCreateUserApartments, QueryPatch


class QueryRepository:
    @staticmethod
    async def create(db: AsyncSession, model: QueryCreate) -> Query:
        query = Query(
            name=model.name,
            input_file=model.input_file,
            sub_queries=list(),
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
        for sub_query in model.sub_queries:
            sub_query_object = SubQuery(
                input_apartments=[Apartment(**apartment.dict()) for apartment in sub_query.input_apartments],
            )
            query.sub_queries.append(sub_query_object)
        db.add(query)
        await db.commit()
        await db.refresh(query)
        return query

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
    async def get_subquery(db: AsyncSession, subguid: UUID4) -> SubQuery:
        res = await db.execute(select(SubQuery).where(SubQuery.guid == subguid).limit(1))
        return res.scalar()

    @staticmethod
    async def set_base(
        db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, stantart_object: QueryCreateBaseApartment
    ) -> Apartment:
        subquery = await QueryRepository.get_subquery(db, subguid)

        if subquery is None:
            raise HTTPException(404, "Подзапрос не найден")
        apartment = Apartment(**dict(filter(lambda apart: apart.guid == 'c5ec9d7f-1637-4c40-b474-aaae9dec6f27', subquery.input_apartments)))
        logger.info(apartment)
        await db.execute(update(SubQuery).where(SubQuery.guid == subguid).values({"standart_object": apartment}))
        await db.commit()
        await db.refresh(subquery)
        logger.info(subquery)


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
