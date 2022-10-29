from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
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
async def upload(file: UploadFile, db: AsyncSession = Depends(get_session)):
    pass