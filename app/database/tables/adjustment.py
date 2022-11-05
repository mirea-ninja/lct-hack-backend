import uuid

from sqlalchemy import Column, Float, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Adjustment(Base):
    __tablename__ = "adjustment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    apartment_guid = Column(UUID(as_uuid=True), ForeignKey("apartment.guid"))
    apartment = relationship("Apartment", back_populates="adjustment", uselist=False)
    trade = Column(Float, nullable=False, default=-450)
    price_trade = Column(Numeric(7, 2), nullable=False)
    floor = Column(Float, nullable=False)
    price_floor = Column(Numeric(7, 2), nullable=False)
    apt_area = Column(Float, nullable=False)
    price_area = Column(Numeric(7, 2), nullable=False)
    kitchen_area = Column(Float, nullable=False)
    price_kitchen = Column(Numeric(7, 2), nullable=False)
    has_balcony = Column(Float, nullable=False)
    price_balcony = Column(Numeric(7, 2), nullable=False)
    distance_to_metro = Column(Float, nullable=False)
    price_metro = Column(Numeric(7, 2), nullable=False)
    quality = Column(Float, nullable=False)
    price_final = Column(Numeric(7, 2), nullable=False)

    analog_calculated_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    analog_user_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    pool_calculated_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    pool_user_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
