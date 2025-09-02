from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new employee
    
    - **name**: Employee name (required)
    - **email**: Employee email (required, must be unique)
    - **position**: Employee position (optional)
    - **department**: Employee department (optional)
    - **start_date**: Employee start date (optional)
    """
    # Check if email already exists
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=schemas.EmployeeListResponse)
def get_employees(
    department: Optional[str] = Query(None, description="Filter by department"),
    start_date_after: Optional[date] = Query(None, description="Filter employees who started after this date"),
    limit: int = Query(100, ge=1, le=1000, description="Number of employees to return"),
    offset: int = Query(0, ge=0, description="Number of employees to skip"),
    db: Session = Depends(get_db)
):
    """
    Get list of employees with optional filtering and pagination
    
    - **department**: Filter by department (optional)
    - **start_date_after**: Filter employees who started after this date (optional)
    - **limit**: Maximum number of employees to return (1-1000, default: 100)
    - **offset**: Number of employees to skip for pagination (default: 0)
    """
    employees, total = crud.get_employees(
        db=db,
        department=department,
        start_date_after=start_date_after,
        limit=limit,
        offset=offset
    )
    
    return schemas.EmployeeListResponse(
        employees=employees,
        total=total,
        limit=limit,
        offset=offset
    )
