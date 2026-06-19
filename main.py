from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Import Models
from models import *

# Import Routers
from routes.auth import router as auth_router
from routes.customers import router as customer_router
from routes.invoices import router as invoice_router
from routes.payments import router as payment_router
from middleware.auth import AuthMiddleware


# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Billing Management System",
    description="Billing & Payment Management API using FastAPI",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(customer_router, prefix="/api/v1")
app.include_router(invoice_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.add_middleware(AuthMiddleware)


@app.get("/")
def home():
    return {
        "message": "Welcome to Billing Management System API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "Running"
    }