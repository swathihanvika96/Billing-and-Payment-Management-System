from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(50), nullable=False)

    role = Column(String(50), default="customer")  # admin/customer

    is_active = Column(Boolean, default=True)