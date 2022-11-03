from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
from app.models import QueryGet
from app.models.enums.file import AllowedFileTypes
from app.services import PoolService
from app.services.auth import get_user_from_access_token, verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


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
    name: Optional[str] = Query(None, description="Название пула"),
    file: UploadFile = File(description="Excel таблица с пулом"),
    user: UUID4 = Depends(get_user_from_access_token),
    db: AsyncSession = Depends(get_session),
    pool_service: PoolService = Depends(),
):
    if not AllowedFileTypes.has_value(file.content_type):
        raise HTTPException(400, detail="Неверный тип файла. Доступные типы: xlsx, xls, csv")

    await pool_service.create(db=db, user=user, name=name, file=file)