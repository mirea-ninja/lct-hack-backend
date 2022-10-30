from .base import BaseEnum


class Segment(str, BaseEnum):
    NEW = "Новостройка"
    MODERN = "Современное"
    OLD = "Старый жилой фонд"
