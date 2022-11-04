from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.connection import get_session
from app.models import ApartmentCreate, ApartmentGet, ApartmentPatch
from app.services import ApartmentService
from app.services.auth import verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    "/query/{id}/subquery/{subid}/apartment",
    response_model=ApartmentGet,
    response_description="Квартира успешно создана",
    status_code=status.HTTP_201_CREATED,
    description="Создать квартиру и вернуть её",
    summary="Создание квартиры",
    # responses={},
)
async def create(
    model: ApartmentCreate,
    db: AsyncSession = Depends(get_session),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.create(db=db, model=model)


@router.get(
    "/query/{id}/subquery/{subid}/apartment",
    response_model=List[ApartmentGet],
    response_description="Успешный возврат списка квартир",
    status_code=status.HTTP_200_OK,
    description="Получить список всех квартир",
    summary="Получение всех квартир",
    # responses={},
)
async def get_all(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.get_all(db=db, guid=id, subid=subid, limit=limit, offset=offset)


@router.get(
    "/query/{id}/subquery/{subid}/apartment/{aid}",
    response_model=ApartmentGet,
    response_description="Успешный возврат квартиры",
    status_code=status.HTTP_200_OK,
    description="Получить квартиры по его id",
    summary="Получение квартиры по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    aid: UUID4 = Path(None, description="Id квартиры"),
    db: AsyncSession = Depends(get_session),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.get(db=db, guid=id, subid=subid, aid=aid)


@router.put(
    "/query/{id}/subquery/{subid}/apartment/{aid}",
    response_model=ApartmentGet,
    response_description="Успешное обновление квартиры",
    status_code=status.HTTP_200_OK,
    description="Изменить квартиры по его id (полное обновление модели)",
    summary="Изменение квартиры по id",
    # responses={},
)
async def update(
    model: ApartmentCreate,
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    aid: UUID4 = Path(None, description="Id квартиры"),
    db: AsyncSession = Depends(get_session),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.update(db=db, guid=id, subid=subid, aid=aid, model=model)


@router.patch(
    "/query/{id}/subquery/{subid}/apartment/{aid}",
    response_model=ApartmentGet,
    response_description="Успешное частичное обновление квартиры",
    status_code=status.HTTP_200_OK,
    description="Изменить квартиру по его id (частисно обновление модели)",
    summary="Изменение квартиры по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: ApartmentPatch,
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    aid: UUID4 = Path(None, description="Id квартиры"),
    db: AsyncSession = Depends(get_session),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.patch(db=db, guid=id, subid=subid, aid=aid, model=model)


@router.delete(
    "/query/{id}/subquery/{subid}/apartment/{aid}",
    response_description="Успешное удаление квартиры",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить квартиры по его id",
    summary="Удаление квартиры по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    aid: UUID4 = Path(None, description="Id квартиры"),
    db: AsyncSession = Depends(get_session),
    apartment_service: ApartmentService = Depends(),
):
    return await apartment_service.delete(db=db, guid=id, subid=subid, aid=aid)
