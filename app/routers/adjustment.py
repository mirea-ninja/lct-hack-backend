from typing import Union

from fastapi import APIRouter, Depends, Path, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import AdjusmentGetValues, AdjustmentGet, AdjustmentPatch
from app.models.enums import AdjustmentType
from app.services import AdjustmentService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


@router.get(
    "/adjustment",
    response_model=AdjusmentGetValues,
    response_description="Успешное частичное обновление квартиры",
    status_code=status.HTTP_200_OK,
    description="Получить список значений корректировок по типу корректировки",
    summary="Получение списка значений корректировок по типу корректировки",
    # responses={},
)
async def get(
    type: AdjustmentType = Query(..., description="Тип корректировки", alias="type"),
    value: Union[float, bool, str] = Query(..., description="Значение"),
    adjustment_service: AdjustmentService = Depends(),
):
    return await adjustment_service.get(type=type, value=value)


@router.patch(
    "/query/{id}/subquery/{subid}/apartment/{aid}/adjustment/{adjid}",
    response_model=AdjustmentGet,
    response_description="Успешное частичное обновление квартиры",
    status_code=status.HTTP_200_OK,
    description="Изменить квартиру по его id (частисно обновление модели)",
    summary="Изменение квартиры по id (только указанные поля будут изменены)",
    # responses={},
)
async def patch(
    model: AdjustmentPatch,
    id: UUID4 = Path(None, description="Id запроса"),
    subid: UUID4 = Path(None, description="Id подзапроса"),
    aid: UUID4 = Path(None, description="Id квартиры"),
    adjid: UUID4 = Path(None, description="Id корректировки"),
    db: AsyncSession = Depends(get_session),
    adjustment_service: AdjustmentService = Depends(),
):
    return await adjustment_service.patch(db=db, guid=id, subid=subid, aid=aid, adjid=adjid, model=model)
