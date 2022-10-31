from decimal import Decimal
from enum import Enum

from pydantic import UUID4, BaseModel, Field


class AdjustmentsBase(BaseModel):
    trade: int = Field(-450, description="Процент чего-то")
    price_trade: Decimal = Field(description="Цена чего-то")
    price_area: Decimal = Field(description="Цена чего-то")
    price_kitchen_area: Decimal = Field(description="Цена чего-то")
    price_balcony: Decimal = Field(description="Цена чего-то")
    price_metro: Decimal = Field(description="Цена чего-то")
    price_final: Decimal = Field(description="Цена чего-то")
    floor: Enum = Field(description="Этаж")
    apt_area: Enum = Field(description="Площадь квартиры")
    kitchen_area: Enum = Field(description="Площадь квартиры")
    has_balcony: Enum = Field(description="Площадь квартиры")
    distance_to_metro: Enum = Field(description="Площадь квартиры")
    quality: Enum = Field(description="Площадь квартиры")

    class Config:
        orm_mode = True


class AdjustmentsGet(AdjustmentsBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры")
