import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class Apartment(Base):
    __tablename__ = "apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    address = Column(String, nullable=False)
    lat = Column(Numeric, nullable=False, default=-1)
    lon = Column(Numeric, nullable=False, default=-1)
    rooms = Column(Integer, nullable=False)
    segment = Column(String, nullable=False)
    floors = Column(Integer, nullable=False)
    walls = Column(String, nullable=False)
    floor = Column(Integer, nullable=False)
    apartment_area = Column(Integer, nullable=False)
    kitchen_area = Column(Integer, nullable=False)
    has_balcony = Column(Boolean, nullable=False)
    distance_to_metro = Column(Integer, nullable=False)
    quality = Column(String, nullable=False)
    m2price = Column(Numeric, nullable=False)
    price = Column(Integer, nullable=False)

    input_apartments_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    standart_object_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    analogs_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    selected_analogs_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
    output_apartments_guid = Column(UUID(as_uuid=True), ForeignKey("sub_query.guid"))
