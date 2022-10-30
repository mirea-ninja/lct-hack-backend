import uuid

from sqlalchemy import Boolean, Column, Enum, Integer, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.models.constants import Quality, Segment, Walls


class Apartment(Base):
    __tablename__ = "apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    address = Column(String, nullable=False)
    rooms = Column(SmallInteger, nullable=False)
    segment = Column(Enum(Segment), nullable=False)
    floors = Column(SmallInteger, nullable=False)
    walls = Column(Enum(Walls), nullable=False)
    floor = Column(SmallInteger, nullable=False)
    apartment_area = Column(Integer, nullable=False)
    kitchen_area = Column(Integer, nullable=False)
    has_balcony = Column(Boolean, nullable=False)
    distance_to_metro = Column(Integer, nullable=False)
    quality = Column(Enum(Quality), nullable=False)

    priced_apartment = relationship("PricedApartment", back_populates="apartment")

    __mapper_args__ = {
        "polymorphic_identity": "apartment",
    }
