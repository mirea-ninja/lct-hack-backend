from collections import namedtuple
from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Adjustment, Apartment, Query, SubQuery
from app.models import ApartmentCreate, QueryCreate, QueryCreateBaseApartment, QueryCreateUserApartments, QueryPatch, \
    AdjustmentCreate
from app.repositories.adjustment import AdjustmentRepository


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
        await db.execute(
            update(Apartment).where(Apartment.guid == stantart_object.guid).values({"standart_object_guid": subguid})
        )
        await db.commit()
        res = await db.execute(select(Apartment).where(Apartment.guid == stantart_object.guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4) -> List[Apartment]:
        subquery = await QueryRepository.get_subquery(db, subguid)
        if len(subquery.analogs) < 5:
            raise HTTPException(503, "Недостаточно аналогов")
        return subquery.analogs

    @staticmethod
    async def create_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, analogs: List[ApartmentCreate]) -> None:
        subquery = await QueryRepository.get_subquery(db, subguid)
        db_analogs = [Apartment(**apartment.dict()) for apartment in analogs]
        subquery.analogs = db_analogs
        await db.commit()
        await db.refresh(subquery)

    @staticmethod
    async def set_analogs(
            db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4, analogs: QueryCreateUserApartments
    ) -> None:
        for analog in analogs.guids:
            await db.execute(
                update(Apartment).where(Apartment.guid == analog).values({"selected_analogs_guid": subguid})
            )
            await db.commit()

    @staticmethod
    async def calculate_analogs(db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4) -> None:
        subquery = await QueryRepository.get_subquery(db, subguid)
        standart_object = subquery.standart_object
        analogs = subquery.analogs

        for analog in analogs:
            model = AdjustmentCreate()
            adjustment = await AdjustmentRepository.create(db, guid, subguid, model)
            analog.adjustment = adjustment
            await db.commit()
            await db.refresh(subquery)

    @staticmethod
    async def calculate_pool(db: AsyncSession, guid: UUID4, subguid: UUID4, user: UUID4) -> None:
        subquery = await QueryRepository.get_subquery(db, subguid)
        standart_object = subquery.standart_object
        input_apartments = subquery.input_apartments