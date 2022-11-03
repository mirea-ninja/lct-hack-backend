from decimal import Decimal

from pydantic import UUID4, BaseModel, Field

from app.models.enums import AptArea, DistanceToMetro, Floor, HasBalcony, KitchenArea, Quality


class AdjustmentBase(BaseModel):
    trade: int = Field(-450,
        description="Корректировка на торг"
    )
    floor: Floor = Field(
        description="Корректировка на этаж"
    )
    apt_area: AptArea = Field(
        description="Корректировка на площадь квартиры"
    )
    kitchen_area: KitchenArea = Field(
        description="Корректировка на площадь кухни"
    )
    has_balcony: HasBalcony = Field(
        description="Корректировка на наличие балкона"
    )
    distance_to_metro: DistanceToMetro = Field(
        description="Корректировка на удаленность от метро"
    )
    quality: Quality = Field(
        description="Корректировка на отделку"
    )

    price_trade: Decimal = Field(
        description="Цена после корректировки на торг"
    )
    price_area: Decimal = Field(
        description="Цена после корректировки на площадь"
    )
    price_kitchen_area: Decimal = Field(
        description="Цена после корректировки на площадь кухни"
    )
    price_balcony: Decimal = Field(
        description="Цена после корректировки на наличие балкона"
    )
    price_metro: Decimal = Field(
        description="Цена после корректировки на удаленность от метро"
    )
    price_final: Decimal = Field(
        description="Цена после корректировки на отделку"
    )


class AdjustmentGet(AdjustmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры, для которой проводилась корректировка автоматически")

    class Config:
        orm_mode = True


class ManualAdjustmentBase(BaseModel):
    trade: int = Field(-450,
        description="Корректировка на торг"
    )
    floor: int = Field(
        description="Корректировка на этаж"
    )
    apt_area: int = Field(
        description="Корректировка на площадь квартиры"
    )
    kitchen_area: int = Field(
        description="Корректировка на площадь кухни"
    )
    has_balcony: int = Field(
        description="Корректировка на наличие балкона"
    )
    distance_to_metro: int = Field(
        description="Корректировка на удаленность от метро"
    )
    quality: int = Field(
        description="Корректировка на отделку"
    )

    price_trade: Decimal = Field(
        description="Цена после корректировки на торг"
    )
    price_area: Decimal = Field(
        description="Цена после корректировки на площадь"
    )
    price_kitchen_area: Decimal = Field(
        description="Цена после корректировки на площадь кухни"
    )
    price_balcony: Decimal = Field(
        description="Цена после корректировки на наличие балкона"
    )
    price_metro: Decimal = Field(
        description="Цена после корректировки на удаленность от метро"
    )
    price_final: Decimal = Field(
        description="Цена после корректировки на отделку"
    )


class ManualAdjustmentGet(ManualAdjustmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры, для которой проводилась корректировка пользователем")

    class Config:
        orm_mode = True
