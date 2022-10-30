from typing import List

from pydantic import UUID4
from sqlalchemy import BigInteger, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast

from app.database.tables import User
from app.models.users import UserCreate


class ArchiveRepository:
    @staticmethod
    async def create(db: AsyncSession, model: UserCreate) -> User:
        query = User(**model.dict())
        db.add(query)
        await db.commit()
        await db.refresh(query)
        return query

    @staticmethod
    async def get_all(db: AsyncSession, offset: int = 0, limit: int = 100) -> List[User]:
        res = await db.execute(select(User).offset(cast(offset, BigInteger)).limit(limit))
        return res.scalars().unique().all()

    @staticmethod
    async def get(db: AsyncSession, guid: UUID4) -> User:
        res = await db.execute(select(User).where(User.guid == guid).limit(1))
        return res.scalar()

    @staticmethod
    async def delete(db: AsyncSession, guid: UUID4) -> None:
        await db.execute(delete(User).where(User.guid == guid))
        await db.commit()
