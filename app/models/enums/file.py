from .base import BaseEnum


class AllowedFileTypes(str, BaseEnum):
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    XLS = "application/vnd.ms-excel"
    CSV = "text/csv"
