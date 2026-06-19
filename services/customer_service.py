from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.customer import Customer


def create_customer(customer, db: Session):

    existing = db.query(Customer).filter(
        Customer.email == customer.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Customer already exists"
        )

    db_customer = Customer(**customer.model_dump())

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_all_customers(db: Session):

    return db.query(Customer).all()


def get_customer(customer_id: int, db: Session):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


def update_customer(customer_id: int, customer_data, db: Session):

    customer = get_customer(customer_id, db)

    for key, value in customer_data.model_dump().items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(customer_id: int, db: Session):

    customer = get_customer(customer_id, db)

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }