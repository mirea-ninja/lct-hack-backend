from __future__ import annotations

from fastapi import HTTPException, Response, UploadFile
from pydantic import UUID4, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.models import ApartmentBase, UserCreate, UserGet, UserPatch
from app.repositories import UsersRepository
from app.storage import get_s3_client


async def send_file(file: bytes, filename: str) -> str:
    async with get_s3_client() as client:
        await client.put_object(
            Bucket=config.STORAGE_BUCKET_NAME,
            Key=f"{filename}",
            Body=file,
        )
    return f"{config.STORAGE_ENDPOINT}/{config.STORAGE_BUCKET_NAME}/{filename}"


class PullService:
    @staticmethod
    async def create(db: AsyncSession, user: UUID4, file: UploadFile):
        read_file = await file.read()
        await send_file(file=read_file, filename=file.filename)
        apartments = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # debug
        return [ApartmentBase(name=apartment) for apartment in apartments]
