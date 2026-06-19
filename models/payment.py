from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        unique=True,
        nullable=False
    )

    amount = Column(Float, nullable=False)

    payment_method = Column(String(100))

    status = Column(String(50), default="Pending")

    invoice = relationship(
        "Invoice",
        back_populates="payment"
    )