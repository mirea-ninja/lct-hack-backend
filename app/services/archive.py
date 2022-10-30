from __future__ import annotations

from fastapi import HTTPException, Response, UploadFile
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.models import UserCreate, UserGet, UserPatch
from app.repositories import UsersRepository
from app.storage import get_s3_client


class ArchiveService:
    @staticmethod
    async def create(db: AsyncSession, user: UUID4, file: UploadFile):
        # model = ArchiveCreate(created_by=user, input_file=storage_link)
        pass

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> list[UserGet]:
        pass

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> UserGet:
        user = await UsersRepository.get(db, guid)
        if user is None:
            raise HTTPException(404, "Архив не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: EmailStr) -> UserGet:
        user = await UsersRepository.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(404, "Архив не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def update(db: AsyncSession, guid: UUID4, model: UserCreate) -> UserGet:
        user = await UsersRepository.update(db, guid, model)
        if user is None:
            raise HTTPException(404, "Архив не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def patch(db: AsyncSession, guid: UUID4, model: UserPatch) -> UserGet:
        user = await UsersRepository.patch(db, guid, model)
        if user is None:
            raise HTTPException(404, "Архив не найден")
        return UserGet.from_orm(user)

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> Response(status_code=204):
        await UsersRepository.delete(db, guid)
        return Response(status_code=204)
