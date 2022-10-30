from typing import List

from pydantic import BaseModel

from app.models.query import QueryBase


class ArchiveBase(BaseModel):
    queries: List[QueryBase]


class ArchiveGet(BaseModel):
    query: QueryBase
