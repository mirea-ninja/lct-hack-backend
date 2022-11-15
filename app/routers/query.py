from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import QueryCreate, QueryGet, QueryPatch
from app.models.enums import SortByEnum
from app.services import QueryService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


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
    sort: SortByEnum = Query(None, description="Cортировка"),
    start: datetime = Query(None, description="Дата начала"),
    end: datetime = Query(None, description="Дата окончания"),
    segment: Optional[list[str]] = Query(None, description="Сегмент"),
    walls: Optional[list[str]] = Query(None, description="Стены"),
    floors_min: int = Query(None, description="Минимальное количество этажей"),
    floors_max: int = Query(None, description="Максимальное количество этажей"),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    query_service: QueryService = Depends(),
):
    return await query_service.get_all(
        db=db,
        sort=sort,
        start=start,
        end=end,
        segment=segment,
        walls=walls,
        floors_min=floors_min,
        floors_max=floors_max,
        limit=limit,
        offset=offset,
    )


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
