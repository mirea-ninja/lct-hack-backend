from pydantic import BaseModel


class QueryBase(BaseModel):
    id: int
