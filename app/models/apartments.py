from decimal import Decimal

from pydantic import UUID4, BaseModel, Field


class ApartmentBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ApartmentGet(BaseModel):
    pass


class PricedApartmentBase(ApartmentBase):
    m2price: Decimal
    price: float


class PricedApartmentGet(PricedApartmentBase):
    guid: UUID4 = Field(description="Уникальный идентификатор квартиры")
