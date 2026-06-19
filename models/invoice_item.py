from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id"),
        nullable=False
    )

    product_name = Column(String(100), nullable=False)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )