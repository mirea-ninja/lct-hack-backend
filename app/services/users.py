from typing import List

from fastapi import Response
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.tables import User
from app.models import UserBase, UserCreate, UserGet, UserPatch
from app.repositories.users import UsersRepository


class UsersService:
    repository: UsersRepository

    def __init__(self, repository: UsersRepository) -> None:
        self.repository = repository

    async def create(self, db: AsyncSession, user: UUID4, model: UserCreate) -> UserBase:
        user = await self.repository.create(db, user, model)
        return UserBase.from_orm(user)

    async def get_all(
        self, db: AsyncSession, user: UUID4, id: UUID4, skip: int = 0, limit: int = 100
    ) -> List[UserBase]:
        users = await self.repository.get_all(db, user, skip=skip, limit=limit)
        return [UserBase.from_orm(u) for u in users]

    async def get(self, db: AsyncSession, user: UUID4, id: UUID4) -> UserGet:
        user = await self.repository.get(db, user, id)
        return UserGet.from_orm(user)

    async def get_user_by_email(self, db: AsyncSession, user: UUID4, email: EmailStr) -> UserBase:
        user = await self.repository.get_user_by_email(db, user, email)
        return UserBase.from_orm(user)

    async def update(self, db: AsyncSession, user: UUID4, id: UUID4, model: UserCreate) -> UserBase:
        user = await self.repository.update(db, user, id, model)
        return UserBase.from_orm(user)

    async def patch(self, db: AsyncSession, user: UUID4, id: UUID4, model: UserPatch) -> UserBase:
        user = await self.repository.patch(db, user, id, model)
        return UserBase.from_orm(user)

    async def delete(self, db: AsyncSession, user: UUID4, id: UUID4) -> Response(status_code=204):
        await self.repository.delete(db, user, id)
