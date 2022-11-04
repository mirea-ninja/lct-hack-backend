from fastapi import APIRouter, Body, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.connection import get_session
from app.fixtures import set_analog_example_value, set_analogs_example_value
from app.models import (
    AdjustmentGet,
    ApartmentCreate,
    ApartmentGet,
    QueryCreate,
    QueryCreateBaseApartment,
    QueryCreateUserApartments,
    QueryGet,
    QueryPatch,
)
from app.services import QueryService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.get(
    "/query",
    response_model=list[QueryGet],
    response_description="Успешный возврат списка запросов",
    status_code=status.HTTP_200_OK,
    description="Получить список всех запросов",
    summary="Получение всех запросов",
    # responses={},
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    query_service: QueryService = Depends(),
):
    return await query_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/query/{id}",
    response_model=QueryGet,
    response_description="Успешный возврат запроса",
    status_code=status.HTTP_200_OK,
    description="Получить запрос по его id",
    summary="Получение запрос по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id запроса"),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.get(db=db, guid=id)


@router.put(
    "/query/{id}",
    response_model=QueryGet,
    response_description="Успешное обновление запроса",
    status_code=status.HTTP_200_OK,
    description="Изменить запрос по его id (полное обновление модели)",
    summary="Изменение запрос по id",
    # responses={},
)
async def update(
    model: QueryCreate,
    id: UUID4 = Path(None, description="Id запроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.update(db=db, guid=id, user=user, model=model)


@router.patch(
    "/query/{id}",
    response_model=QueryGet,
    response_description="Успешное частичное обновление запроса",
    status_code=status.HTTP_200_OK,
    description="Изменить запрос по его id (частичное обновление модели)",
    summary="Изменение запрос по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: QueryPatch,
    id: UUID4 = Path(None, description="Id запроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.patch(db=db, guid=id, user=user, model=model)


@router.delete(
    "/query/{id}",
    response_description="Успешное удаление запроса",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить запрос по его id",
    summary="Удаление запрос по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id запроса"),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.delete(db=db, guid=id)

@router.post(
    "/query/{id}/subquery/{subid}/base-apartment",
    response_model=ApartmentGet,
    response_description="Эталонный объект успешно установлен",
    status_code=status.HTTP_201_CREATED,
    description="Установить эталонный объект для подзапроса",
    summary="Установка эталонного объекта",
    # responses={},
)
async def set_base(
    analog: QueryCreateBaseApartment = Body(None, description="Список аналогов", example=set_analog_example_value),
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.set_base(db=db, guid=id, subguid=subid, user=user, analog=analog)


@router.get(
    "/query/{id}/subquery/{subid}/analogs",
    response_model=list[ApartmentGet],
    response_description="Успешный возврат списка аналогов",
    status_code=status.HTTP_200_OK,
    description="Получить список аналогов для подзапроса",
    summary="Получение аналогов для подзапроса",
    # responses={},
)
async def get_analogs(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.get_analogs(db=db, guid=id, subguid=subid)


@router.post(
    "/query/{id}/subquery/{subid}/analogs",
    response_description="Успешная установка аналогов",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Установить аналоги для подзапроса",
    summary="Установка аналогов для подзапроса",
    # responses={},
)
async def create_analogs(
    analogs: list[ApartmentCreate],
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.create_analogs(db=db, guid=id, subguid=subid, analogs=analogs)


@router.post(
    "/query/{id}/subquery/{subid}/user-analogs",
    response_model=AdjustmentGet,
    response_description="Расчет успешно завершен",
    status_code=status.HTTP_201_CREATED,
    description="Установить подзапросу выбранные аналоги, провести расчет и вернуть результат",
    summary="Установка аналогов и расчет",
    # responses={},
)
async def set_analogs(
    analogs: QueryCreateUserApartments = Body(None, description="Список аналогов", example=set_analogs_example_value),
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.set_analogs(db=db, guid=id, subguid=subid, user=user, analogs=analogs)
