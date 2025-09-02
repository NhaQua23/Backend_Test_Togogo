from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from typing import Optional, List
from . import models, schemas

def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_employee_by_email(db: Session, email: str) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employees(
    db: Session, 
    department: Optional[str] = None,
    start_date_after: Optional[date] = None,
    limit: int = 100, 
    offset: int = 0
) -> tuple[List[models.Employee], int]:
    query = db.query(models.Employee)
    
    if department:
        query = query.filter(models.Employee.department == department)
    
    if start_date_after:
        query = query.filter(models.Employee.start_date >= start_date_after)
    
    total = query.count()
    
    employees = query.offset(offset).limit(limit).all()
    
    return employees, total

def get_work_shift(
    db: Session, 
    employee_id: int, 
    work_day: date
) -> Optional[models.WorkShift]:
    return db.query(models.WorkShift).filter(
        and_(
            models.WorkShift.employee_id == employee_id,
            models.WorkShift.work_day == work_day
        )
    ).first()

def create_work_shift(
    db: Session, 
    work_shift: schemas.WorkShiftCreate
) -> models.WorkShift:
    db_work_shift = models.WorkShift(**work_shift.dict())
    db.add(db_work_shift)
    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift

def update_work_shift(
    db: Session, 
    db_work_shift: models.WorkShift, 
    shift: models.ShiftType
) -> models.WorkShift:
    db_work_shift.shift = shift
    db.commit()
    db.refresh(db_work_shift)
    return db_work_shift

def upsert_work_shift(
    db: Session, 
    work_shift_data: schemas.WorkShiftCreate
) -> tuple[models.WorkShift, str]:
    existing_shift = get_work_shift(
        db, 
        work_shift_data.employee_id, 
        work_shift_data.work_day
    )
    
    if existing_shift:
        updated_shift = update_work_shift(db, existing_shift, work_shift_data.shift)
        return updated_shift, "updated"
    else:
        new_shift = create_work_shift(db, work_shift_data)
        return new_shift, "created"

def get_employee_by_id(db: Session, employee_id: int) -> Optional[models.Employee]:
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()
