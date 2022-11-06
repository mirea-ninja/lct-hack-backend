from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database import get_session
from app.models import QueryExport, QueryGet
from app.models.enums.file import AllowedFileTypes
from app.services import PoolService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.post(
    "/pool",
    response_model=QueryGet,
    response_description="Пул успешно загружен и обработан",
    status_code=status.HTTP_201_CREATED,
    description="Загрузить новый пул в сервис",
    summary="Загрузка пула",
    # responses={},
)
async def create(
    name: Optional[str] = Query(None, description="Название запроса"),
    file: UploadFile = File(description="Excel таблица с пулом"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    pool_service: PoolService = Depends(),
):
    if not AllowedFileTypes.has_value(file.content_type):
        raise HTTPException(400, detail="Неверный тип файла. Доступные типы: xlsx, xls, csv")

    return await pool_service.create(db=db, user=user, name=name, file=file)


@router.get(
    "/export",
    response_model=QueryExport,
    response_description="Пул успешно обработан и экспортирован",
    status_code=status.HTTP_200_OK,
    description="Экспортировать пул в файл",
    summary="Экспорт пула",
    # responses={},
)
async def export(
    id: UUID4 = Query(description="Id запроса"),
    include_adjustments: bool = Query(False, description="Включить корректировки", alias="includeAdjustments"),
    split_by_lists: bool = Query(False, description="Разбить данные по листам", alias="splitByLists"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    pool_service: PoolService = Depends(),
):
    return await pool_service.export(
        db=db, guid=id, include_adjustments=include_adjustments, split_by_lists=split_by_lists, user=user
    )
