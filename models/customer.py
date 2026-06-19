from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(20))

    address = Column(String(200))

    is_active = Column(Boolean, default=True)

    invoices = relationship(
        "Invoice",
        back_populates="customer",
        cascade="all, delete"
    )