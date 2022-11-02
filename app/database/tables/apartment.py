import uuid

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base
from app.models.enums import RepairType, Segment, Walls


class Apartment(Base):
    __tablename__ = "apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    sub_query_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"), nullable=False)
    address = Column(String, nullable=False)
    lat = Column(Numeric, nullable=False)
    lon = Column(Numeric, nullable=False)
    rooms = Column(Integer, nullable=False)
    segment = Column(Enum(Segment), nullable=False)
    floors = Column(Integer, nullable=False)
    walls = Column(Enum(Walls), nullable=False)
    floor = Column(Integer, nullable=False)
    apartment_area = Column(Integer, nullable=False)
    kitchen_area = Column(Integer, nullable=False)
    has_balcony = Column(Boolean, nullable=False)
    distance_to_metro = Column(Integer, nullable=False)
    quality = Column(Enum(RepairType), nullable=False)
    m2price = Column(Numeric, nullable=False)
    price = Column(Integer, nullable=False)
