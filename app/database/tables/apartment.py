import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Apartment(Base):
    __tablename__ = "apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    address = Column(String, nullable=False)
    lat = Column(Numeric, nullable=False, default=-1)
    lon = Column(Numeric, nullable=False, default=-1)
    link = Column(String, nullable=True)
    rooms = Column(Integer, nullable=False)
    segment = Column(String, nullable=False)
    floors = Column(Integer, nullable=False)
    walls = Column(String, nullable=True)
    floor = Column(Integer, nullable=False)
    apartment_area = Column(Integer, nullable=False)
    kitchen_area = Column(Integer, nullable=True)
    has_balcony = Column(Boolean, nullable=True)
    distance_to_metro = Column(Integer, nullable=True)
    quality = Column(String, nullable=True)
    m2price = Column(Numeric, nullable=True)
    price = Column(Integer, nullable=True)

    adjustment = relationship("Adjustment", back_populates="apartment", uselist=False)

    input_apartments_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    standart_object_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    analogs_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    selected_analogs_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    output_apartments_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
