import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Query(Base):
    __tablename__ = "query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    apartments = relationship("Apartment", back_populates="query")
    standart_object = relationship("PricedApartment", back_populates="query")
    analogs = relationship("PricedApartment", back_populates="query")
    selected_analogs = relationship("PricedApartment", back_populates="query")
    adjustments_analog_calculated = relationship("Adjustments", back_populates="query")
    adjustments_analog_user = relationship("Adjustments", back_populates="query")
    adjustments_pool_calculated = relationship("Adjustments", back_populates="query")
    adjustments_pool_user = relationship("Adjustments", back_populates="query")
    result = relationship("PricedApartment", back_populates="query")
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=False)
    archive = relationship("Archive", back_populates="query")
