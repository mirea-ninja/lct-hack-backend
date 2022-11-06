from fastapi import APIRouter, Depends, Path
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.config import config
from app.database.connection import get_session
from app.models import AdjustmentGet, AdjustmentPatch
from app.services import AdjustmentService
from app.services.auth import verify_access_token

router = APIRouter(prefix=config.BACKEND_PREFIX, dependencies=[Depends(verify_access_token)])


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
