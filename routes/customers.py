from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.customer import Customer
from models.invoice import Invoice

from schemas.customer import CustomerCreate, CustomerResponse

# Import your JWT dependency
from utils.dependencies import get_current_admin

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# -------------------------
# Create Customer
# -------------------------
@router.post("/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


# -------------------------
# Get All Customers
# -------------------------
@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    return db.query(Customer).all()


# -------------------------
# Get Customer By ID
# -------------------------
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# -------------------------
# Update Customer
# -------------------------
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    db_customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not db_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db_customer.name = customer.name
    db_customer.email = customer.email
    db_customer.phone = customer.phone
    db_customer.address = customer.address

    db.commit()
    db.refresh(db_customer)

    return db_customer


# -------------------------
# Delete Customer
# -------------------------
@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}


# -------------------------
# Activate Customer
# -------------------------
@router.put("/{customer_id}/activate")
def activate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = True

    db.commit()

    return {
        "message": "Customer activated"
    }


# -------------------------
# Deactivate Customer
# -------------------------
@router.put("/{customer_id}/deactivate")
def deactivate_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = False

    db.commit()

    return {
        "message": "Customer deactivated"
    }


# -------------------------
# Get Customer Invoices
# -------------------------
@router.get("/{customer_id}/invoices")
def get_customer_invoices(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if not customer.is_active:
        raise HTTPException(
            status_code=400,
            detail="Customer is inactive"
        )

    invoices = db.query(Invoice).filter(
        Invoice.customer_id == customer_id
    ).all()

    return invoices