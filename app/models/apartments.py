from pydantic import BaseModel


class ApartmentBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
