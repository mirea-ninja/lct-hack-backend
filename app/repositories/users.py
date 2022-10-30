from typing import List

from pydantic import UUID4, EmailStr
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.tables import User
from app.models.users import UserCreate, UserPatch


class UsersRepository:
    @staticmethod
    async def create(db: AsyncSession, model: UserCreate) -> User:
        user = User(**model.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[User]:
        res = await db.execute(select(User).offset(offset).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> User:
        res = await db.execute(select(User).where(User.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: EmailStr) -> User:
        res = await db.execute(select(User).where(User.email == email).limit(1))
        return res.scalar()

    @staticmethod
    async def update(db: AsyncSession, user: UUID4, guid: UUID4, model: UserCreate) -> None:
        raise NotImplementedError

    @staticmethod
    async def patch(db: AsyncSession, user: UUID4, guid: UUID4, model: UserPatch) -> None:
        raise NotImplementedError

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(User).where(User.guid == guid))
        await db.commit()
