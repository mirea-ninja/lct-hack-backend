from typing import List

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database.connection import get_session
from app.models import UserCreate, UserGet, UserPatch
from app.services import UsersService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.patch(
    "/query/{id}/set/base",
    # response_model=UserGet,
    response_description="Эталонный объект успешно установлен",
    status_code=status.HTTP_201_CREATED,
    description="Установить эталонный объект для запроса",
    summary="Уставнока эталонного объекта",
    # responses={},
)
async def set_base(
    model: UserCreate,
    db: AsyncSession = Depends(get_session),
):
    pass


@router.get(
    "/query/{id}/analogs",
    # response_model=List[UserGet],
    response_description="Успешный возврат списка аналогов",
    status_code=status.HTTP_200_OK,
    description="Получить список аналогов для запроса",
    summary="Получение аналогов для запроса",
    # responses={},
)
async def analogs(
    db: AsyncSession = Depends(get_session),
):
    pass


@router.patch(
    "/query/{id}/set/analogs",
    # response_model=UserGet,
    response_description="Расчет успешно завершен",
    status_code=status.HTTP_201_CREATED,
    description="Установить запросу выбранные аналоги, провести расчет и вернуть результат",
    summary="Уставнока аналогов и расчет",
    # responses={},
)
async def set_analogs(
    model: UserCreate,
    db: AsyncSession = Depends(get_session),
):
    pass
