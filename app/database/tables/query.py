import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Query(Base):
    __tablename__ = "query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=True)
    sub_queries = relationship("SubQuery", back_populates="query", uselist=True, lazy="joined")
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class SubQuery(Base):
    __tablename__ = "sub_query"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    query_guid = Column(UUID(as_uuid=True), ForeignKey("query.guid"), nullable=False)
    query = relationship("Query", back_populates="sub_queries", uselist=False, lazy="joined")

    input_apartments = relationship("Apartment", lazy="joined", foreign_keys="Apartment.input_apartments_guid")
    standart_object = relationship(
        "Apartment", uselist=False, lazy="joined", foreign_keys="Apartment.standart_object_guid"
    )
    analogs = relationship("Apartment", lazy="joined", foreign_keys="Apartment.analogs_guid")
    selected_analogs = relationship("Apartment", lazy="joined", foreign_keys="Apartment.selected_analogs_guid")
    adjustments_analog_calculated = relationship(
        "Adjustment", lazy="joined", foreign_keys="Adjustment.analog_calculated_guid"
    )
    adjustments_analog_user = relationship("Adjustment", lazy="joined", foreign_keys="Adjustment.analog_user_guid")
    adjustments_pool_calculated = relationship(
        "Adjustment", lazy="joined", foreign_keys="Adjustment.pool_calculated_guid"
    )
    adjustments_pool_user = relationship("Adjustment", lazy="joined", foreign_keys="Adjustment.pool_user_guid")
    output_apartments = relationship("Apartment", lazy="joined", foreign_keys="Apartment.output_apartments_guid")
