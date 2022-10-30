from __future__ import annotations

from fastapi import HTTPException, Response
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UserCreate, UserGet, UserPatch
from app.repositories import UsersRepository


class UsersService:
    @staticmethod
    async def create(db: AsyncSession, model: UserCreate) -> UserGet:
        user = await UsersRepository.create(db, model)
        if user is None:
            raise HTTPException(409, "Пользователь с таким email уже существует")
        return UserGet.from_orm(user)

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[UserGet]:
        users = await UsersRepository.get_all(db, offset=offset, limit=limit)
        if users is None:
            raise HTTPException(404, "Пользователи не найдены")
        return [UserGet.from_orm(u) for u in users]

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> UserGet:
        user = await UsersRepository.get(db, guid)
        if user is None:
            raise HTTPException(404, "Пользователь не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: EmailStr) -> UserGet:
        user = await UsersRepository.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(404, "Пользователь не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: UserCreate) -> UserGet:
        user = await UsersRepository.update(db, guid, model)
        if user is None:
            raise HTTPException(404, "Пользователь не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: UserPatch) -> UserGet:
        user = await UsersRepository.patch(db, guid, model)
        if user is None:
            raise HTTPException(404, "Пользователь не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await UsersRepository.delete(db, guid)
        return Response(status_code=204)
