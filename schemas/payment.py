from pydantic import BaseModel, Field, field_validator


class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str

    @field_validator("payment_method")
    @classmethod
    def validate_method(cls, value):
        methods = ["UPI", "Card", "Wallet"]
        if value not in methods:
            raise ValueError("Payment method must be UPI, Card or Wallet")
        return value


class PaymentResponse(BaseModel):
    id: int
    invoice_id: int
    amount: float
    payment_method: str
    status: str

    class Config:
        from_attributes = True