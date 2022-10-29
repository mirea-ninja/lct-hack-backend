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
            raise HTTPException(409, "User is already exists")
        return UserGet.from_orm(user)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[UserGet]:
        users = await UsersRepository.get_all(db, skip=skip, limit=limit)
        if users is None:
            raise HTTPException(404, "Users not found")
        return [UserGet.from_orm(u) for u in users]

    @staticmethod
    async def get(db: AsyncSession, id: UUID4) -> UserGet:
        user = await UsersRepository.get(db, id)
        if user is None:
            raise HTTPException(404, "User not found")
        return UserGet.from_orm(user)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: EmailStr) -> UserGet:
        user = await UsersRepository.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(404, "User not found")
        return UserGet.from_orm(user)

    @staticmethod
    async def update(db: AsyncSession, user: UUID4, id: UUID4, model: UserCreate) -> UserGet:
        user = await UsersRepository.update(db, user, id, model)
        if user is None:
            raise HTTPException(404, "User not found")
        return UserGet.from_orm(user)

    @staticmethod
    async def patch(db: AsyncSession, user: UUID4, id: UUID4, model: UserPatch) -> UserGet:
        user = await UsersRepository.patch(db, user, id, model)
        if user is None:
            raise HTTPException(404, "User not found")
        return UserGet.from_orm(user)

    @staticmethod
    async def delete(db: AsyncSession, id: UUID4) -> Response(status_code=204):
        await UsersRepository.delete(db, id)
        return Response(status_code=204)
