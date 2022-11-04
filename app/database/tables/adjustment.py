import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class Adjustment(Base):
    __tablename__ = "adjustment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
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

    analog_calculated_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    analog_user_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    pool_calculated_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    pool_user_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
