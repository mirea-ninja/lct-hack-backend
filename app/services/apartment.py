from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ApartmentCreate, ApartmentGet, ApartmentPatch
from app.repositories import ApartmentRepository


class ApartmentService:
    @staticmethod
    async def create(db: AsyncSession, model: ApartmentCreate) -> ApartmentGet:
        apartment = await ApartmentRepository.create(db, model)
        return ApartmentGet.from_orm(apartment)

    @staticmethod
    async def get_all(
        db: AsyncSession, guid: UUID4, subid: UUID4, offset: int = 0, limit: int = 100
    ) -> list[ApartmentGet]:
        apartments = await ApartmentRepository.get_all(db, offset=offset, limit=limit)
        if apartments is None:
            raise HTTPException(404, "Квартиры не найдены")
        return [ApartmentGet.from_orm(a) for a in apartments]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4) -> ApartmentGet:
        apartment = await ApartmentRepository.get(db, guid)
        if apartment is None:
            raise HTTPException(404, "Квартира не найдена")
        return ApartmentGet.from_orm(apartment)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, model: ApartmentCreate) -> ApartmentGet:
        apartment = await ApartmentRepository.update(db, guid, model)
        if apartment is None:
            raise HTTPException(404, "Квартира не найдена")
        return ApartmentGet.from_orm(apartment)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4, model: ApartmentPatch) -> ApartmentGet:
        apartment = await ApartmentRepository.patch(db, guid, model)
        if apartment is None:
            raise HTTPException(404, "Квартира не найдена")
        return ApartmentGet.from_orm(apartment)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4, subid: UUID4, aid: UUID4) -> Response(status_code=204):
        await ApartmentRepository.delete(db, guid)
        return Response(status_code=204)
