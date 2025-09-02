from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/workshifts", tags=["work shifts"])

@router.post("/", response_model=schemas.WorkShiftUpsertResponse)
def create_or_update_work_shift(
    work_shift: schemas.WorkShiftCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update work shift for an employee
    
    - **employee_id**: ID of the employee (required)
    - **work_day**: Work date in YYYY-MM-DD format (required)
    - **shift**: Shift type - morning, afternoon, or full_day (required)
    
    If a work shift already exists for the employee on the given date, it will be updated.
    If no work shift exists, a new one will be created.
    """
    # Check if employee exists
    employee = crud.get_employee_by_id(db, work_shift.employee_id)
    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )
    
    # Create or update work shift
    db_work_shift, status = crud.upsert_work_shift(db=db, work_shift_data=work_shift)
    
    return schemas.WorkShiftUpsertResponse(
        status=status,
        work_shift=db_work_shift
    )
