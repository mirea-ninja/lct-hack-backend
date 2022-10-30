from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
from app.models.enums.file import AllowedFileTypes
from app.services.auth import verify_access_token

router = APIRouter(dependencies=[Depends(verify_access_token)])


@router.post(
    "/pull",
    # response_model=TypeModel,
    status_code=status.HTTP_200_OK,
    description="Загрузить новый пул в сервис",
    summary="Загрузка пула",
    # responses={},
)
async def upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_session)):
    if not AllowedFileTypes.has_value(file.content_type):
        raise HTTPException(400, detail="Неверный тип файла. Доступные типы: xlsx, xls, csv")
