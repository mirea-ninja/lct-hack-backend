from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, HttpUrl

from app.models import AdjustmentsGet, ApartmentGet, PricedApartmentGet
from app.models.utils import optional


class SubQueryBase(BaseModel):
    apartments: List[ApartmentGet] = Field(description="Список квартир во входном файле")
    standart_object: PricedApartmentGet = Field(description="Стандартный объект")
    analogs: List[PricedApartmentGet] = Field(description="Список подобранных аналогов")
    selected_analogs: List[PricedApartmentGet] = Field(description="Список выбранных аналогов")
    adjustments_analog_calculated: List[AdjustmentsGet] = Field(description="Список расчитаных аналогов")
    adjustments_analog_user: List[AdjustmentsGet] = Field(
        description="Список расчитаных аналогов, исправленных " "пользователем"
    )
    adjustments_pool_calculated: List[AdjustmentsGet] = Field(description="Список настроек пула")
    adjustments_pool_user: List[AdjustmentsGet] = Field(description="Список настроек пула")
    output_apartments: List[PricedApartmentGet] = Field(description="Список выходных квартир")


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
    queries: List[SubQueryGet] = Field(description="Список подзапросов")
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
class QueryPatch(QueryBase):
    pass
