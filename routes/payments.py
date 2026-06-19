from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session

from database import get_db
from models.invoice import Invoice
from models.payment import Payment
from schemas.payment import PaymentCreate
from utils.dependencies import get_current_admin, get_current_customer
from background.email import send_payment_email

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/pay/{invoice_id}")
def pay_invoice(
    invoice_id: int,
    payment: PaymentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_customer),
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    existing = (
        db.query(Payment)
        .filter(Payment.invoice_id == invoice_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Invoice already paid",
        )

    if payment.amount != invoice.total_amount:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must match invoice amount",
        )

    if payment.payment_method not in ["UPI", "Card", "Wallet"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment method",
        )

    db_payment = Payment(
        invoice_id=invoice.id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        status="Success",
    )

    db.add(db_payment)

    invoice.status = "Paid"

    db.commit()
    db.refresh(db_payment)

    background_tasks.add_task(
        send_payment_email,
        invoice.id,
    )

    return {
        "message": "Payment Successful",
        "payment": db_payment,
    }


@router.get("/")
def get_all_payments(
    method: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    query = db.query(Payment)

    if method:
        query = query.filter(
            Payment.payment_method == method
        )

    total_records = query.count()

    payments = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "data": payments,
    }


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_customer),
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    return payment


@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted successfully"
    }
