from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, HttpUrl

from app.models import AdjustmentGet, ApartmentBase, ApartmentGet
from app.models.utils import optional


class SubQueryBase(BaseModel):
    input_apartments: Optional[List[ApartmentBase]] = Field(description="Список квартир в подзапросе")
    standart_object: Optional[ApartmentBase] = Field(description="Эталонный объект")
    analogs: Optional[List[ApartmentBase]] = Field(description="Список подобранных аналогов")
    selected_analogs: Optional[List[ApartmentBase]] = Field(description="Список выбранных аналогов")
    adjustments_analog_calculated: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для аналогов"
    )
    adjustments_analog_user: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для аналогов, исправленных пользователем"
    )
    adjustments_pool_calculated: Optional[List[AdjustmentGet]] = Field(description="Список корректировок для пула")
    adjustments_pool_user: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для пула, исправленных пользователем"
    )
    output_apartments: Optional[List[ApartmentBase]] = Field(description="Список выходных квартир")


class SubQueryCreate(SubQueryBase):
    pass


class SubQueryGet(BaseModel):
    guid: UUID4 = Field(description="Уникальный идентификатор подзапроса")
    input_apartments: Optional[List[ApartmentGet]] = Field(description="Список квартир в подзапросе")
    standart_object: Optional[ApartmentGet] = Field(description="Эталонный объект")
    analogs: Optional[List[ApartmentGet]] = Field(description="Список подобранных аналогов")
    selected_analogs: Optional[List[ApartmentGet]] = Field(description="Список выбранных аналогов")
    adjustments_analog_calculated: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для аналогов"
    )
    adjustments_analog_user: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для аналогов, исправленных пользователем"
    )
    adjustments_pool_calculated: Optional[List[AdjustmentGet]] = Field(description="Список корректировок для пула")
    adjustments_pool_user: Optional[List[AdjustmentGet]] = Field(
        description="Список корректировок для пула, исправленных пользователем"
    )
    output_apartments: Optional[List[ApartmentGet]] = Field(description="Список выходных квартир")

    class Config:
        orm_mode = True


@optional
class SubQueryPatch(SubQueryBase):
    pass


class QueryBase(BaseModel):
    name: Optional[str] = Field(None, description="Название запроса")
    input_file: HttpUrl = Field(description="Ссылка на файл с входными данными")
    output_file: Optional[HttpUrl] = Field(None, description="Ссылка на файл с выходными данными")


class QueryCreate(QueryBase):
    sub_queries: List[SubQueryCreate] = Field(description="Список подзапросов")
    created_by: UUID4 = Field(description="Уникальный идентификатор пользователя, создавшего запись")
    updated_by: UUID4 = Field(description="Уникальный идентификатор пользователя, обновившего запись")


class QueryGet(QueryBase):
    guid: UUID4 = Field(description="Уникальный идентификатор записи")
    sub_queries: List[SubQueryGet] = Field(description="Список подзапросов")
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
    guid: UUID4 = Field(description="Уникальный идентификатор эталонного объекта")


class QueryCreateUserApartments(BaseModel):
    guids: List[UUID4] = Field(description="Уникальные идентификаторы аналогов, устанавливаемых пользователем")
