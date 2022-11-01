from decimal import Decimal

from pydantic import UUID4, BaseModel, Field

from app.models.enums import AptArea, DistanceToMetro, Floor, HasBalcony, KitchenArea, Quality


class AdjustmentBase(BaseModel):
    trade: int = Field(-450, description="Процент чего-то")
    price_trade: Decimal = Field(description="Цена чего-то")
    price_area: Decimal = Field(description="Цена чего-то")
    price_kitchen_area: Decimal = Field(description="Цена чего-то")
    price_balcony: Decimal = Field(description="Цена чего-то")
    price_metro: Decimal = Field(description="Цена чего-то")
    price_final: Decimal = Field(description="Цена чего-то")
    floor: Floor = Field(description="Этаж")
    apt_area: AptArea = Field(description="Площадь квартиры")
    kitchen_area: KitchenArea = Field(description="Площадь квартиры")
    has_balcony: HasBalcony = Field(description="Площадь квартиры")
    distance_to_metro: DistanceToMetro = Field(description="Площадь квартиры")
    quality: Quality = Field(description="Площадь квартиры")


class AdjustmentGet(AdjustmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры")

    class Config:
        orm_mode = True


class ManualAdjustmentBase(BaseModel):
    trade: int = Field(-450, description="Процент чего-то")
    price_trade: Decimal = Field(description="Цена чего-то")
    price_area: Decimal = Field(description="Цена чего-то")
    price_kitchen_area: Decimal = Field(description="Цена чего-то")
    price_balcony: Decimal = Field(description="Цена чего-то")
    price_metro: Decimal = Field(description="Цена чего-то")
    price_final: Decimal = Field(description="Цена чего-то")
    floor: int = Field(description="Этаж")
    apt_area: int = Field(description="Площадь квартиры")
    kitchen_area: int = Field(description="Площадь квартиры")
    has_balcony: int = Field(description="Площадь квартиры")
    distance_to_metro: int = Field(description="Площадь квартиры")
    quality: int = Field(description="Площадь квартиры")


class ManualAdjustmentGet(ManualAdjustmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры")

    class Config:
        orm_mode = True
