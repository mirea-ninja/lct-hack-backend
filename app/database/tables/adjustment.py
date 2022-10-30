import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.models.constants.adjustments import *


class Adjustment(Base):
    __tablename__ = "adjustment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    trade = Column(Integer, nullable=False, default=-450)
    price_trade = Column(Numeric(7, 2), nullable=False)
    price_floor = Column(Numeric(7, 2), nullable=False)
    price_area = Column(Numeric(7, 2), nullable=False)
    price_kitchen_area = Column(Numeric(7, 2), nullable=False)
    price_balcony = Column(Numeric(7, 2), nullable=False)
    price_metro = Column(Numeric(7, 2), nullable=False)
    price_final = Column(Numeric(7, 2), nullable=False)
    floor = Column(Enum(FLOOR), nullable=False)
    apt_area = Column(
        Enum(APT_AREA),
        nullable=False,
    )
    kitchen_area = Column(Enum(KITCHEN_AREA), nullable=False)
    has_balcony = Column(Enum(HAS_BALCONY), nullable=False)
    distance_to_metro = Column(
        Enum(DISTANCE_TO_METRO),
        nullable=False,
    )
    quality = Column(Enum(QUALITY), nullable=False)

    query_guid = Column(UUID(as_uuid=True), ForeignKey("query.guid"), nullable=False)
    query = relationship("Query", back_populates="adjustments")
