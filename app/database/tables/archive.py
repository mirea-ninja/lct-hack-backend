import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Archive(Base):
    __tablename__ = "archive"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    input_file = Column(String, nullable=False)
    output_file = Column(String, nullable=False)
    query = relationship("Query", back_populates="archive", uselist=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
