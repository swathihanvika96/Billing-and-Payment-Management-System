from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    amount = Column(Float, default=0)

    tax = Column(Float, default=0)

    discount = Column(Float, default=0)

    total_amount = Column(Float)

    due_date = Column(Date)

    status = Column(
        String(50),
        default="Pending"
    )

    customer = relationship(
        "Customer",
        back_populates="invoices"
    )

    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete"
    )

    payment = relationship(
        "Payment",
        back_populates="invoice",
        uselist=False
    )