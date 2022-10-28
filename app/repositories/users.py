from typing import List

from pydantic import UUID4, EmailStr
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound

from app.database.connection import get_session
from app.database.tables import User
from app.models.users import UserCreate, UserPatch


class UsersRepository:
    async def create(self, db: AsyncSession, user: UUID4, model: UserCreate) -> User:
        pass

    async def get_all(self, db: AsyncSession, user: UUID4, skip: int = 0, limit: int = 100) -> List[User]:
        res = await db.execute(select(User).offset(skip).limit(limit))
        return res.scalars().unique().all()

    async def get(self, db: AsyncSession, user: UUID4, id: UUID4) -> User:
        res = await db.execute(select(User).where(User.id == id).limit(1))
        return res.scalar()

    async def get_user_by_email(self, db: AsyncSession, user: UUID4, email: EmailStr) -> User:
        res = await db.execute(select(User).where(User.email == email).limit(1))
        return res.scalar()

    async def update(self, db: AsyncSession, user: UUID4, id: UUID4, model: UserCreate) -> None:
        raise NotImplementedError

    async def patch(self, db: AsyncSession, user: UUID4, id: UUID4, model: UserPatch) -> None:
        raise NotImplementedError

    async def delete(self, db: AsyncSession, user: UUID4, id: UUID4) -> None:
        async with get_session() as session:
            await session.execute(delete(User).where(User.id == id))
            await session.commit()
