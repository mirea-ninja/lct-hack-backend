from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
from app.models import ArchiveBase, ArchiveGet
from app.services import ArchiveService
from app.services.auth import verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.get(
    "/archive",
    response_model=ArchiveBase,
    response_description="Успешный возврат записей в архиве",
    status_code=status.HTTP_200_OK,
    description="Получить список всех записей в архиве",
    summary="Получение всех записей в архиве",
    # responses={},
)
async def get_all(
    db: AsyncSession = Depends(get_session),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    archive_service: ArchiveService = Depends(),
):
    return await archive_service.get_all(db=db, limit=limit, offset=offset)


@router.get(
    "/archive/{id}",
    response_model=ArchiveGet,
    response_description="Успешный возврат записи в архиве",
    status_code=status.HTTP_200_OK,
    description="Получить запись по его id",
    summary="Получение записи в архиве по id",
    # responses={},
)
async def get(
    id: UUID4 = Path(None, description="Id записи в архиве"),
    db: AsyncSession = Depends(get_session),
    archive_service: ArchiveService = Depends(),
):
    return await archive_service.get(db=db, guid=id)


@router.delete(
    "/archive/{id}",
    response_description="Успешное удаление записи в архиве",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удалить запись по id",
    summary="Удаление записи в архиве по id",
    # responses={},
)
async def delete(
    id: UUID4 = Path(None, description="Id записи в архиве"),
    db: AsyncSession = Depends(get_session),
    archive_service: ArchiveService = Depends(),
):
    return await archive_service.delete(db=db, guid=id)
