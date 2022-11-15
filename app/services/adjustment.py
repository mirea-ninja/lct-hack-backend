from __future__ import annotations

from typing import Union

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdjusmentGetValues, AdjustmentGet, AdjustmentPatch
from app.models.enums import AdjustmentType
from app.repositories import AdjustmentRepository, QueryRepository


class AdjustmentService:
    @staticmethod
    async def get(type: AdjustmentType, value: Union[float, bool, str]) -> AdjusmentGetValues:
        adjustments = await QueryRepository.get_adjustments(type, value)
        if adjustments is None:
            raise HTTPException(404, "Корректировки не найдены")
        return AdjusmentGetValues(adjustments=adjustments)

    @staticmethod
    async def patch(
        db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, adjid: UUID4, model: AdjustmentPatch
    ) -> AdjustmentGet:
        adjustment = await AdjustmentRepository.patch(db, guid, subid, aid, adjid, model)
        if adjustment is None:
            raise HTTPException(404, "Корректировка не найдена")
        return AdjustmentGet.from_orm(adjustment)
