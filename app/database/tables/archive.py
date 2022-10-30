import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Archive(Base):
    __tablename__ = "archive"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    query = relationship("Query", back_populates="archive")
    query_guid = Column(UUID(as_uuid=True), ForeignKey("query.guid"), nullable=False)
