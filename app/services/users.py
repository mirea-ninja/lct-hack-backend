from __future__ import annotations

from fastapi import Depends, Response
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables import User
from app.models import UserBase, UserCreate, UserGet, UserPatch
from app.repositories import UsersRepository


class UsersService:
    @staticmethod
    async def create(db: AsyncSession, model: UserCreate) -> UserGet | None:
        user = await UsersRepository.create(db, model)
        if user:
            return UserGet.from_orm(user)
        return None

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserGet] | None:
        users = await UsersRepository.get_all(db, skip=skip, limit=limit)
        if users:
            return [UserGet.from_orm(u) for u in users]
        return None

    @staticmethod
    async def get(db: AsyncSession, id: UUID4) -> UserGet | None:
        user = await UsersRepository.get(db, id)
        if user:
            return UserGet.from_orm(user)
        return None

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: EmailStr) -> UserGet | None:
        user = await UsersRepository.get_user_by_email(db, email)
        if user:
            return UserGet.from_orm(user)
        return None

    @staticmethod
    async def update(db: AsyncSession, user: UUID4, id: UUID4, model: UserCreate) -> UserGet | None:
        user = await UsersRepository.update(db, user, id, model)
        if user:
            return UserGet.from_orm(user)
        return None

    @staticmethod
    async def patch(db: AsyncSession, user: UUID4, id: UUID4, model: UserPatch) -> UserGet | None:
        user = await UsersRepository.patch(db, user, id, model)
        if user:
            return UserGet.from_orm(user)
        return None

    @staticmethod
    async def delete(db: AsyncSession, id: UUID4) -> Response(status_code=204):
        await UsersRepository.delete(db, id)
        return Response(status_code=204)
