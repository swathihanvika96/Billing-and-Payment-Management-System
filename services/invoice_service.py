from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer
from models.invoice import Invoice
from models.invoice_item import InvoiceItem


def create_invoice(invoice, db: Session):

    customer = db.query(Customer).filter(
        Customer.id == invoice.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if not customer.is_active:
        raise HTTPException(
            status_code=400,
            detail="Customer is inactive"
        )

    if invoice.due_date <= date.today():
        raise HTTPException(
            status_code=400,
            detail="Due date must be in the future"
        )

    subtotal = sum(
        item.quantity * item.price
        for item in invoice.items
    )

    total = subtotal + invoice.tax - invoice.discount

    if total <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid invoice amount"
        )

    db_invoice = Invoice(
        customer_id=invoice.customer_id,
        amount=subtotal,
        tax=invoice.tax,
        discount=invoice.discount,
        total_amount=total,
        due_date=invoice.due_date,
        status="Pending"
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.items:

        db_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )

        db.add(db_item)

    db.commit()

    return db_invoice


def get_invoice(invoice_id: int, db: Session):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


def get_all_invoices(db: Session):

    return db.query(Invoice).all()


def delete_invoice(invoice_id: int, db: Session):

    invoice = get_invoice(invoice_id, db)

    db.delete(invoice)
    db.commit()

    return {
        "message": "Invoice deleted"
    }