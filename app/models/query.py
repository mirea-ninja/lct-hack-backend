from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, HttpUrl

from app.models import AdjustmentGet, ApartmentGet, ManualAdjustmentGet
from app.models.utils import optional


class SubQueryBase(BaseModel):
    input_apartments: List[ApartmentGet] = Field(description="Список квартир во входном файле")
    standart_object: ApartmentGet = Field(description="Стандартный объект")
    analogs: List[ApartmentGet] = Field(description="Список подобранных аналогов")
    selected_analogs: List[ApartmentGet] = Field(description="Список выбранных аналогов")
    adjustments_analog_calculated: List[AdjustmentGet] = Field(description="Список расчитаных аналогов")
    adjustments_analog_user: List[ManualAdjustmentGet] = Field(
        description="Список расчитаных аналогов, исправленных " "пользователем"
    )
    adjustments_pool_calculated: List[AdjustmentGet] = Field(description="Список настроек пула")
    adjustments_pool_user: List[ManualAdjustmentGet] = Field(description="Список настроек пула")
    output_apartments: List[ApartmentGet] = Field(description="Список выходных квартир")


class SubQueryCreate(SubQueryBase):
    pass


class SubQueryGet(SubQueryBase):
    guid: UUID4 = Field(description="Уникальный идентификатор подзапроса")

    class Config:
        orm_mode = True


@optional
class SubQueryPatch(SubQueryBase):
    pass


class QueryBase(BaseModel):
    name: Optional[str] = Field(None, description="Название запроса")
    sub_queries: List[SubQueryGet] = Field(description="Список подзапросов")
    input_file: HttpUrl = Field(description="Ссылка на файл с входными данными")
    output_file: Optional[HttpUrl] = Field(None, description="Ссылка на файл с выходными данными")


class QueryCreate(QueryBase):
    pass


class QueryGet(QueryBase):
    guid: UUID4 = Field(description="Уникальный идентификатор записи")
    created_by: UUID4 = Field(description="Уникальный идентификатор пользователя, создавшего запись")
    updated_by: UUID4 = Field(description="Уникальный идентификатор пользователя, обновившего запись")
    created_at: datetime = Field(description="Время создания записи")
    updated_at: datetime = Field(description="Время последнего обновления записи")

    class Config:
        orm_mode = True


@optional
class QueryPatch(QueryCreate):
    pass


class QueryCreateBaseApartment(BaseModel):
    analog: UUID4 = Field(description="Уникальный идентификатор аналога")


class QueryCreateUserApartments(BaseModel):
    analogs: List[UUID4] = Field(description="Уникальные идентификатор аналогов")
