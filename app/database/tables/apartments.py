import uuid

from sqlalchemy import Column, DateTime, String, func, Integer, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base
from app.models.enums import Walls, Quality, Segment


class Apartment(Base):
    __tablename__ = "apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    address = Column(String, nullable=False)
    rooms = Column(Integer, nullable=False)
    segment = Column(Enum(Segment), nullable=False)
    floors = Column(Integer, nullable=False)
    walls = Column(Enum(Walls), nullable=False)
    floor = Column(Integer, nullable=False)
    apt_area = Column(Integer, nullable=False)
    kitchen_area = Column(Integer, nullable=False)
    has_balcony = Column(Boolean, nullable=False)
    distance_to_metro = Column(Integer, nullable=False)
    quality = Column(Enum(Quality), nullable=False)
