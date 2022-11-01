import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base
from app.models.enums import AptArea, DistanceToMetro, Floor, HasBalcony, KitchenArea, Quality


class Adjustment(Base):
    __tablename__ = "adjustment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    sub_query_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"), nullable=False)
    trade = Column(Integer, nullable=False, default=-450)
    price_trade = Column(Numeric(7, 2), nullable=False)
    floor = Column(Enum(Floor), nullable=False)
    price_floor = Column(Numeric(7, 2), nullable=False)
    apt_area = Column(Enum(AptArea), nullable=False)
    price_area = Column(Numeric(7, 2), nullable=False)
    kitchen_area = Column(Enum(KitchenArea), nullable=False)
    price_kitchen = Column(Numeric(7, 2), nullable=False)
    has_balcony = Column(Enum(HasBalcony), nullable=False)
    price_balcony = Column(Numeric(7, 2), nullable=False)
    distance_to_metro = Column(Enum(DistanceToMetro), nullable=False)
    price_metro = Column(Numeric(7, 2), nullable=False)
    quality = Column(Enum(Quality), nullable=False)
    price_final = Column(Numeric(7, 2), nullable=False)


class ManualAdjustment(Base):
    __tablename__ = "manual_adjustment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    sub_query_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"), nullable=False)
    trade = Column(Integer, nullable=False, default=-450)
    price_trade = Column(Numeric(7, 2), nullable=False)
    floor = Column(Integer, nullable=False)
    price_floor = Column(Numeric(7, 2), nullable=False)
    apt_area = Column(Integer, nullable=False)
    price_area = Column(Numeric(7, 2), nullable=False)
    kitchen_area = Column(Integer, nullable=False)
    price_kitchen = Column(Numeric(7, 2), nullable=False)
    has_balcony = Column(Integer, nullable=False)
    price_balcony = Column(Numeric(7, 2), nullable=False)
    distance_to_metro = Column(Integer, nullable=False)
    price_metro = Column(Numeric(7, 2), nullable=False)
    quality = Column(Integer, nullable=False)
    price_final = Column(Numeric(7, 2), nullable=False)
