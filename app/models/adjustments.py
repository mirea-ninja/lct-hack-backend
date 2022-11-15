from pydantic import UUID4, BaseModel, Field

from app.models.utils import optional


class AdjustmentBase(BaseModel):
    trade: float = Field(description="Корректировка на торг")
    floor: float = Field(description="Корректировка на этаж")
    apt_area: float = Field(description="Корректировка на площадь квартиры")
    kitchen_area: float = Field(description="Корректировка на площадь кухни", alias="kitchenArea")
    has_balcony: float = Field(description="Корректировка на наличие балкона", alias="hasBalcony")
    distance_to_metro: float = Field(description="Корректировка на удаленность от метро", alias="distanceToMetro")
    quality: float = Field(description="Корректировка на отделку")

    price_trade: int = Field(description="Цена после корректировки на торг", alias="priceTrade")
    price_floor: int = Field(description="Цена после корректировки на торг", alias="priceFloor")
    price_area: int = Field(description="Цена после корректировки на площадь", alias="priceArea")
    price_kitchen: int = Field(description="Цена после корректировки на площадь кухни", alias="priceKitchen")
    price_balcony: int = Field(description="Цена после корректировки на наличие балкона", alias="priceBalcony")
    price_metro: int = Field(description="Цена после корректировки на удаленность от метро", alias="priceMetro")
    price_final: int = Field(description="Цена после корректировки на отделку", alias="priceFinal")

    class Config:
        allow_population_by_field_name = True


class AdjustmentGet(AdjustmentBase):
    guid: UUID4 = Field(
        description="Уникальный идентификатор квартиры, для которой проводилась корректировка автоматически"
    )

    class Config:
        orm_mode = True


class AdjustmentCreate(AdjustmentBase):
    pass


@optional
class AdjustmentPatch(AdjustmentCreate):
    pass


class AdjusmentGetValues(BaseModel):
    adjustments: list[float] = Field(description="Список корректировок")
