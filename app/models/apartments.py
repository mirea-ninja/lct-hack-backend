from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class ApartmentBase(BaseModel):
    address: str = Field(description="Адрес квартиры")
    lat: Optional[Decimal] = Field(description="Широта")
    lon: Optional[Decimal] = Field(description="Долгота")
    rooms: int = Field(description="Количество комнат")
    segment: str = Field(description="Тип жилья")
    floors: int = Field(description="Количество этажей")
    walls: str = Field(description="Материал стен")
    floor: int = Field(description="Этаж")
    apartment_area: int = Field(description="Площадь квартиры")
    kitchen_area: int = Field(description="Площадь кухни")
    has_balcony: bool = Field(description="Наличие балкона")
    distance_to_metro: int = Field(description="Расстояние до метро")
    quality: str = Field(description="Отделка")
    m2price: Optional[Decimal] = Field(0, description="Цена за квадратный метр")
    price: Optional[int] = Field(0, description="Цена квартиры")


class ApartmentGet(ApartmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры")

    class Config:
        orm_mode = True


class ApartmentCreate(ApartmentBase):
    pass


@optional
class ApartmentPatch(ApartmentCreate):
    pass
