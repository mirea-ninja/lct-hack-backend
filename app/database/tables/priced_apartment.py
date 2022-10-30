import uuid

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .apartment import Apartment


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html
class PricedApartment(Apartment):
    __tablename__ = "priced_apartment"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    m2price = Column(Numeric(7, 2), nullable=False)
    price = Column(Integer, nullable=False)

    apartment_guid = Column(Integer, ForeignKey("apartment.guid"))
    apartment = relationship("Apartment", back_populates="priced_apartment")

    __mapper_args__ = {
        "polymorphic_identity": "priced_apartment",
    }
