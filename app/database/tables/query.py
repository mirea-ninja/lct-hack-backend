import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Query(Base):
    __tablename__ = "query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    archive_guid = Column(UUID(as_uuid=True), ForeignKey("archive.guid"))
    archive = relationship("Archive", back_populates="query")
    name = Column(String, nullable=True)
    # apartments = relationship("Apartment", back_populates="query", lazy="joined", uselist=False) # one-to-many
    # standart_object = relationship("Apartment", back_populates="query", uselist=False) # one-to-one
    # analogs = relationship("PricedApartment", back_populates="query", lazy="joined", uselist=False) # one-to-many
    # adjustments_analog_calculated = relationship("AnalogAdjustments", back_populates="query", uselist=False) # one-to-one
    # adjustments_analog_user = relationship("AnalogAdjustments", back_populates="query", uselist=False) # one-to-one
    # adjustments_pool_calculated = relationship("Adjustments", back_populates="query", uselist=False) # one-to-one
    # adjustments_pool_user = relationship("Adjustments", back_populates="query", uselist=False) # one-to-one
    # result = relationship("PricedApartment", back_populates="query", uselist=False) # one-to-many
