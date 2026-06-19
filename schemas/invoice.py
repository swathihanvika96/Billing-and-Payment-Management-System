from datetime import date
from typing import List

from pydantic import BaseModel, Field, field_validator


class InvoiceItemCreate(BaseModel):
    product_name: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class InvoiceCreate(BaseModel):
    customer_id: int
    tax: float = 0
    discount: float = 0
    due_date: date
    items: List[InvoiceItemCreate]

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        if value <= date.today():
            raise ValueError("Due date must be in the future")
        return value


class InvoiceItemResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: int
    customer_id: int
    amount: float
    tax: float
    discount: float
    total_amount: float
    due_date: date
    status: str
    items: List[InvoiceItemResponse]

    class Config:
        from_attributes = True