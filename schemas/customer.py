from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str


class CustomerResponse(CustomerCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True