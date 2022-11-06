from __future__ import annotations

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdjustmentGet, AdjustmentPatch
from app.repositories import AdjustmentRepository


class AdjustmentService:
    @staticmethod
    async def patch(
        db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, adjid: UUID4, model: AdjustmentPatch
    ) -> AdjustmentGet:
        adjustment = await AdjustmentRepository.patch(db, guid, subid, aid, adjid, model)
        if adjustment is None:
            raise HTTPException(404, "Корректировка не найдена")
        return AdjustmentGet.from_orm(adjustment)
