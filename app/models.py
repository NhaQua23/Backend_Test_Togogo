from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class ShiftType(enum.Enum):
    """Enum for work shift types"""
    morning = "morning"
    afternoon = "afternoon"
    full_day = "full_day"

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    position = Column(String)
    department = Column(String)
    start_date = Column(Date)
    
    # Relationship with work shifts
    work_shifts = relationship("WorkShift", back_populates="employee")

class WorkShift(Base):
    __tablename__ = "work_shifts"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    work_day = Column(Date, nullable=False)
    shift = Column(Enum(ShiftType), nullable=False)
    
    # Relationship with employee
    employee = relationship("Employee", back_populates="work_shifts")
