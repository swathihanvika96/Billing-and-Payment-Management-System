from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.invoice import Invoice
from models.payment import Payment


def pay_invoice(invoice_id: int, payment, db: Session):

    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    existing = db.query(Payment).filter(
        Payment.invoice_id == invoice_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid"
        )

    if payment.amount != invoice.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment amount mismatch"
        )

    db_payment = Payment(
        invoice_id=invoice.id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="Success"
    )

    db.add(db_payment)

    invoice.status = "Paid"

    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_payment(payment_id: int, db: Session):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


def get_all_payments(db: Session):

    return db.query(Payment).all()