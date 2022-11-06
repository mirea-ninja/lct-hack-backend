from pydantic import UUID4, BaseModel, Field


class AdjustmentBase(BaseModel):
    trade: float = Field(description="Корректировка на торг")
    floor: float = Field(description="Корректировка на этаж")
    apt_area: float = Field(description="Корректировка на площадь квартиры")
    kitchen_area: float = Field(description="Корректировка на площадь кухни")
    has_balcony: float = Field(description="Корректировка на наличие балкона")
    distance_to_metro: float = Field(description="Корректировка на удаленность от метро")
    quality: float = Field(description="Корректировка на отделку")

    price_trade: float = Field(description="Цена после корректировки на торг")
    price_floor: float = Field(description="Цена после корректировки на торг")
    price_area: float = Field(description="Цена после корректировки на площадь")
    price_kitchen: float = Field(description="Цена после корректировки на площадь кухни")
    price_balcony: float = Field(description="Цена после корректировки на наличие балкона")
    price_metro: float = Field(description="Цена после корректировки на удаленность от метро")
    price_final: float = Field(description="Цена после корректировки на отделку")


class AdjustmentGet(AdjustmentBase):
    guid: UUID4 = Field(
        description="Уникальный идентификатор квартиры, для которой проводилась корректировка автоматически"
    )

    class Config:
        orm_mode = True


class AdjustmentCreate(AdjustmentBase):
    pass


class AdjustmentPatch(AdjustmentCreate):
    pass
