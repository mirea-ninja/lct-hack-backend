from app.models.enums import BaseEnum


class SortByEnum(str, BaseEnum):
    ASC = "asc"
    DESC = "desc"
