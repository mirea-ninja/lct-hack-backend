from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import BigInteger, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.tables import Adjustment
from app.models import AdjustmentPatch, AdjustmentCreate
from app.repositories.query import QueryRepository


class AdjustmentRepository:
    @staticmethod
    async def create(db: AsyncSession, guid: UUID4, subid: UUID4, model: AdjustmentCreate) -> Adjustment:
        adjustment = Adjustment(**model.dict())
        db.add(adjustment)
        await db.commit()
        await db.refresh(adjustment)
        subquery = await QueryRepository.get_subquery(db, subid)
        subquery.analogs.adjustments = adjustment
        await db.commit()
        await db.refresh(subquery)
        return adjustment

    @staticmethod
    async def get(
            db: AsyncSession,
            guid: UUID4,
            subid: UUID4,
            aid: UUID4,
    ) -> Adjustment:
        res = await db.execute(select(Adjustment).where(Adjustment.guid == aid).limit(1))
        return res.scalar()

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, model: AdjustmentPatch) -> Adjustment:
        adjustment = await AdjustmentRepository.get(db, guid, subid, aid)

        if adjustment is None:
            raise HTTPException(404, "Корректировки не найдены")

        if model is None or not model.dict(exclude_unset=True):
            raise HTTPException(400, "Должно быть задано хотя бы одно новое поле модели")

        await db.execute(update(Adjustment).where(Adjustment.guid == aid).values(**model.dict()))
        await db.commit()
        await db.refresh(adjustment)

        return adjustment
