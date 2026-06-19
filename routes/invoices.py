from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.customer import Customer
from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from schemas.invoice import InvoiceCreate
from utils.dependencies import get_current_admin

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def update_invoice_status(invoice):
    if invoice.status == "Paid":
        return
    invoice.status = "Overdue" if invoice.due_date < date.today() else "Pending"


@router.post("/")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
    if not customer:
        raise HTTPException(404, "Customer not found")
    if not customer.is_active:
        raise HTTPException(400, "Customer is inactive")
    if invoice.due_date <= date.today():
        raise HTTPException(400, "Due date should be in future")

    subtotal = sum(i.quantity * i.price for i in invoice.items)
    total = subtotal + invoice.tax - invoice.discount
    if total <= 0:
        raise HTTPException(400, "Total amount should be greater than zero")

    db_invoice = Invoice(
        customer_id=invoice.customer_id,
        amount=subtotal,
        tax=invoice.tax,
        discount=invoice.discount,
        total_amount=total,
        due_date=invoice.due_date,
        status="Pending",
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    for item in invoice.items:
        db.add(
            InvoiceItem(
                invoice_id=db_invoice.id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
            )
        )
    db.commit()

    return {
        "message": "Invoice Created Successfully",
        "invoice_id": db_invoice.id,
        "total_amount": total,
    }


@router.get("/")
def get_all_invoices(
    status: str | None = Query(None),
    due_date_before: date | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    query = db.query(Invoice)

    if status:
        query = query.filter(Invoice.status == status)
    if due_date_before:
        query = query.filter(Invoice.due_date <= due_date_before)

    total_records = query.count()

    invoices = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    for inv in invoices:
        update_invoice_status(inv)
    db.commit()

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "data": invoices,
    }


@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    invoice = (
        db.query(Invoice)
        .options(joinedload(Invoice.items))
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(404, "Invoice not found")

    update_invoice_status(invoice)
    db.commit()

    return {
        "invoice_id": invoice.id,
        "customer_id": invoice.customer_id,
        "subtotal": invoice.amount,
        "tax": invoice.tax,
        "discount": invoice.discount,
        "total_amount": invoice.total_amount,
        "due_date": invoice.due_date,
        "status": invoice.status,
        "items": invoice.items,
    }


@router.put("/{invoice_id}")
def update_invoice(
    invoice_id: int,
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(404, "Invoice not found")

    customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
    if not customer:
        raise HTTPException(404, "Customer not found")
    if not customer.is_active:
        raise HTTPException(400, "Customer is inactive")

    subtotal = sum(i.quantity * i.price for i in invoice.items)
    total = subtotal + invoice.tax - invoice.discount
    if total <= 0:
        raise HTTPException(400, "Invalid invoice total")

    db_invoice.customer_id = invoice.customer_id
    db_invoice.amount = subtotal
    db_invoice.tax = invoice.tax
    db_invoice.discount = invoice.discount
    db_invoice.total_amount = total
    db_invoice.due_date = invoice.due_date

    db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()

    for item in invoice.items:
        db.add(
            InvoiceItem(
                invoice_id=invoice_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price,
            )
        )

    db.commit()
    return {"message": "Invoice updated successfully"}


@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(404, "Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}
