from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List
from .models import ShiftType

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    position: Optional[str] = None
    department: Optional[str] = None
    start_date: Optional[date] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True

class WorkShiftBase(BaseModel):
    employee_id: int
    work_day: date
    shift: ShiftType

class WorkShiftCreate(WorkShiftBase):
    pass

class WorkShiftResponse(WorkShiftBase):
    id: int
    
    class Config:
        from_attributes = True

class WorkShiftUpsertResponse(BaseModel):
    status: str  # "created" or "updated"
    work_shift: WorkShiftResponse

class EmployeeListResponse(BaseModel):
    """Response schema for employee list with pagination"""
    employees: List[EmployeeResponse]
    total: int
    limit: int
    offset: int
