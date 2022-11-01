import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Query(Base):
    __tablename__ = "query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=True)
    sub_queries = relationship("SubQuery", back_populates="query", uselist=False, lazy="joined")
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SubQuery(Base):
    __tablename__ = "sub_query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    query_guid = Column(UUID(as_uuid=True), ForeignKey("query.guid"), nullable=False)
    query = relationship("Query", back_populates="sub_queries")
    input_apartments = relationship("Apartment", lazy="joined")
    standart_object = relationship("Apartment", uselist=False, lazy="joined")
    analogs = relationship("Apartment", lazy="joined")
    selected_analogs = relationship("Apartment", lazy="joined")
    adjustments_analog_calculated = relationship("Adjustment", lazy="joined")
    adjustments_analog_user = relationship("ManualAdjustment", lazy="joined")
    adjustments_pool_calculated = relationship("Adjustment", lazy="joined")
    adjustments_pool_user = relationship("ManualAdjustment", lazy="joined")
    output_apartments = relationship("Apartment", lazy="joined")
