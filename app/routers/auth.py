from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_session
from app.models import Token, UserAuth, UserCreate
from app.services import AuthService

router = APIRouter()


@router.post(
    "/signin",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    description="Войти в сервис и получить токен",
    summary="Вход в сервис",
    # responses={},
)
async def signin(model: UserAuth, db: AsyncSession = Depends(get_session), auth_service: AuthService = Depends()):
    return await auth_service.signin(db=db, model=model)


@router.post(
    "/signup",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    description="Зарегистирироваться в сервисе и получить токен",
    summary="Регистрация в сервисе",
    # responses={},
)
async def signup(model: UserCreate, db: AsyncSession = Depends(get_session), auth_service: AuthService = Depends()):
    return await auth_service.signup(db=db, model=model)
