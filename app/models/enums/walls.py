from .base import BaseEnum


class Walls(str, BaseEnum):
    BRICK = "Кирпич"
    PANEL = "Панель"
    MONOLITH = "Монолит"
