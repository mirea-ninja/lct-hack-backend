from typing import List

from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.models import UserCreate, UserGet
from app.services import UsersService

router = APIRouter()


@router.post(
    "/user",
    summary="Создание нового пользователя",
    response_model=UserGet,
)
async def create(
    model: UserCreate,
    db: AsyncSession = Depends(get_session),
    user: UUID4 = Depends(),
):
    return await UsersService.create(db, user, model)


@router.get(
    "/user",
    summary="Получение всех пользователей",
    response_model=List[UserGet],
)
async def get_all():
    pass


@router.get(
    "/user/{id}",
    summary="Получение пользователя по id",
    response_model=UserGet,
)
async def get():
    pass


@router.put(
    "/user/{id}",
    summary="Изменение пользователя по id",
    response_model=UserGet,
)
async def update():
    pass


@router.patch(
    "/user/{id}",
    summary="Изменение пользователя по id (только указанные поля будут изменены)",
    response_model=UserGet,
)
async def patch():
    pass


@router.delete(
    "/user/{id}",
    summary="Удаление пользователя по id",
    response_model=UserGet,
)
async def delete():
    pass
