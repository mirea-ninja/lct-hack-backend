from fastapi import APIRouter, Body, Depends, Path
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.fixtures import set_analog_example_value, set_analogs_example_value
from app.models import (
    ApartmentCreate,
    ApartmentGet,
    QueryCreateBaseApartment,
    QueryCreateUserApartments,
    QueryGet,
    SubQueryGet,
)
from app.services import QueryService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


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
    response_model=SubQueryGet,
    response_description="Аналоги успешно установлены",
    status_code=status.HTTP_201_CREATED,
    description="Установить подзапросу выбранные аналоги",
    summary="Установка аналогов для подзапроса",
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


@router.post(
    "/query/{id}/subquery/{subid}/calculate-analogs",
    response_model=QueryGet,
    response_description="Аналоги успешно рассчитаны",
    status_code=status.HTTP_200_OK,
    description="Рассчитать аналоги для подзапроса",
    summary="Расчет аналогов для подзапроса",
    # responses={},
)
async def calculate_analogs(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.calculate_analogs(db=db, guid=id, subguid=subid, user=user)


@router.post(
    "/query/{id}/subquery/{subid}/recalculate-analogs",
    response_model=QueryGet,
    response_description="Аналоги успешно рассчитаны",
    status_code=status.HTTP_200_OK,
    description="Рассчитать аналоги для подзапроса",
    summary="Расчет аналогов для подзапроса",
    # responses={},
)
async def recalculate_analogs(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.recalculate_analogs(db=db, guid=id, subguid=subid, user=user)


@router.post(
    "/query/{id}/subquery/{subid}/calculate-pool",
    response_model=QueryGet,
    response_description="Пул успешно рассчитан",
    status_code=status.HTTP_200_OK,
    description="Рассчитать пул для подзапроса",
    summary="Расчет пула для подзапроса",
    # responses={},
)
async def calculate_pool(
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    query_service: QueryService = Depends(),
):
    return await query_service.calculate_pool(db=db, guid=id, subguid=subid, user=user)
