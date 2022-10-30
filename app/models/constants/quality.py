from .base_enum import BaseEnum


class Quality(str, BaseEnum):
    NO_FINISH = "Без отделки"
    ECONOM = "Эконом"
    IMPROVED = "Улучшенный"
