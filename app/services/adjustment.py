from __future__ import annotations

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdjustmentGet, AdjustmentPatch
from app.models.enums import AdjustmentType
from app.repositories import AdjustmentRepository, QueryRepository


class AdjustmentService:
    @staticmethod
    async def get(db: AsyncSession, type: AdjustmentType, value: float) -> AdjustmentGet:
        adjustment = await QueryRepository.get_adjustments(type, value)
        logger.info(f"AdjustmentService.get: {adjustment}")
        if adjustment is None:
            raise HTTPException(404, "Корректировка не найдена")
        return AdjustmentGet.from_orm(adjustment)

    @staticmethod
    async def patch(
        db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, adjid: UUID4, model: AdjustmentPatch
    ) -> AdjustmentGet:
        adjustment = await AdjustmentRepository.patch(db, guid, subid, aid, adjid, model)
        if adjustment is None:
            raise HTTPException(404, "Корректировка не найдена")
        return AdjustmentGet.from_orm(adjustment)
