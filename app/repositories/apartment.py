from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import Apartment
from app.models import ApartmentCreate, ApartmentPatch


class ApartmentRepository:
    @staticmethod
    async def create(db: AsyncSession, guid: UUID4, subid: UUID4, model: ApartmentCreate) -> Apartment:
        pass

    @staticmethod
    async def get_all(
        db: AsyncSession, guid: UUID4, subid: UUID4, offset: int = 0, limit: int = 100
    ) -> List[Apartment]:
        res = await db.execute(select(Apartment).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4,) -> Apartment:
        res = await db.execute(select(Apartment).where(Apartment.guid == aid).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, model: ApartmentCreate) -> Apartment:
        apartment = await ApartmentRepository.get(db, guid, subid, aid)

        if apartment is None:
            raise HTTPException(404, "Квартира не найдена")

        await db.execute(update(Apartment).where(Apartment.guid == aid).values(**model.dict()))
        await db.commit()
        await db.refresh(apartment)

        return apartment

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, model: ApartmentPatch) -> Apartment:
        apartment = await ApartmentRepository.get(db, guid, subid, aid)

        if apartment is None:
            raise HTTPException(404, "Квартира не найдена")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Apartment).where(Apartment.guid == aid).values(**model.dict()))
        await db.commit()
        await db.refresh(apartment)

        return apartment

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4) -> None:
        await db.execute(delete(Apartment).where(Apartment.guid == aid))
        await db.commit()
