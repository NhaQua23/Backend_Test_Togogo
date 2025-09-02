from fastapi import FastAPI
from .database import engine
from . import models
from .routers import employees, workshifts

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System",
    description="A FastAPI backend for managing employees and work shifts",
    version="1.0.0"
)

app.include_router(employees.router)
app.include_router(workshifts.router)

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Employee Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
