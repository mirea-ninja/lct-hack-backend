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
    input_file: HttpUrl = Field(description="Ссылка на файл с входными данными", alias="inputFile")
    output_file: Optional[HttpUrl] = Field(None, description="Ссылка на файл с выходными данными", alias="outputFile")

    class Config:
        allow_population_by_field_name = True


class QueryCreate(QueryBase):
    sub_queries: List[SubQueryCreate] = Field(description="Список подзапросов", alias="subQueries")
    created_by: UUID4 = Field(description="Уникальный идентификатор пользователя, создавшего запись", alias="createdBy")
    updated_by: UUID4 = Field(
        description="Уникальный идентификатор пользователя, обновившего запись", alias="updatedBy"
    )

    class Config:
        allow_population_by_field_name = True


class QueryGet(QueryBase):
    guid: UUID4 = Field(description="Уникальный идентификатор записи")
    sub_queries: List[SubQueryGet] = Field(description="Список подзапросов", alias="subQueries")
    created_by: UUID4 = Field(description="Уникальный идентификатор пользователя, создавшего запись", alias="createdBy")
    updated_by: UUID4 = Field(
        description="Уникальный идентификатор пользователя, обновившего запись", alias="updatedBy"
    )
    created_at: datetime = Field(description="Время создания записи", alias="createdAt")
    updated_at: datetime = Field(description="Время последнего обновления записи", alias="updatedAt")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


@optional
class QueryPatch(QueryCreate):
    pass


class QueryCreateBaseApartment(BaseModel):
    guid: UUID4 = Field(description="Уникальный идентификатор эталонного объекта")


class QueryCreateUserApartments(BaseModel):
    guids: List[UUID4] = Field(description="Уникальные идентификаторы аналогов, устанавливаемых пользователем")


class QueryExport(BaseModel):
    link: HttpUrl = Field(example="https://example.com/", description="Ссылка на файл с выходными данными")
