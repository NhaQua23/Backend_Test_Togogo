# Employee Management System - Technical Report

## 1. Diễn giải Logic Tổng thể và Thiết kế Database

### Tại sao thiết kế như vậy?

Hệ thống được thiết kế theo **mô hình quan hệ** để quản lý nhân viên và ca làm việc với các nguyên tắc:

- **Tách biệt quan tâm**: Nhân viên và ca làm việc là 2 thực thể độc lập
- **Tính mở rộng**: Dễ dàng thêm tính năng mới (phòng ban, dự án, lương...)
- **Tính toàn vẹn**: Ràng buộc khóa ngoại đảm bảo tính nhất quán dữ liệu

### Mối quan hệ giữa các bảng

```
employees (1) -----> (n) work_shifts
    |                       |
    id (PK) <-----------> employee_id (FK)
```

**Quan hệ One-to-Many**: Một nhân viên có thể có nhiều ca làm việc, nhưng mỗi ca chỉ thuộc về một nhân viên.

### Schema Database

```sql
-- Bảng employees
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    position VARCHAR,
    department VARCHAR,
    start_date DATE
);

-- Bảng work_shifts
CREATE TABLE work_shifts (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    work_day DATE NOT NULL,
    shift VARCHAR CHECK (shift IN ('morning', 'afternoon', 'full_day'))
);
```

## 2. Giải thích Code Quan trọng

### 2.1 Models (SQLAlchemy)

```python
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # ... other fields

    # Relationship - tự động load work_shifts khi query Employee
    work_shifts = relationship("WorkShift", back_populates="employee")
```

**Điểm quan trọng:**

- `unique=True` trên email đảm bảo không trùng lặp
- `index=True` tăng tốc độ tìm kiếm
- `relationship()` tạo liên kết ORM giữa các bảng

### 2.2 Schemas (Pydantic)

```python
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr  # Tự động validate format email
    position: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True  # Cho phép convert từ SQLAlchemy model
```

**Tại sao tách Create và Response?**

- **Create**: Chỉ chứa dữ liệu input từ client
- **Response**: Bao gồm thêm `id` được tạo bởi database

### 2.3 CRUD Operations

```python
def upsert_work_shift(db: Session, work_shift_data: schemas.WorkShiftCreate):
    existing_shift = get_work_shift(db, work_shift_data.employee_id, work_shift_data.work_day)

    if existing_shift:
        # Update existing
        return update_work_shift(db, existing_shift, work_shift_data.shift), "updated"
    else:
        # Create new
        return create_work_shift(db, work_shift_data), "created"
```

**Logic Upsert**: Kiểm tra tồn tại trước → Update hoặc Create → Trả về status rõ ràng.

### 2.4 API Endpoints (FastAPI)

```python
@router.post("/", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    # Validate email unique
    if crud.get_employee_by_email(db, email=employee.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_employee(db=db, employee=employee)
```

**Validation layers:**

1. **Pydantic**: Validate format dữ liệu (email, required fields)
2. **Business logic**: Validate business rules (email unique)
3. **Database**: Validate constraints (foreign keys)

## 3. Quy trình Hoạt động API

### Luồng xử lý Request → Response

```
Client Request
    ↓
FastAPI Router (validate URL params)
    ↓
Pydantic Schema (validate request body)
    ↓
Business Logic (validate business rules)
    ↓
CRUD Operations (database operations)
    ↓
SQLAlchemy Models (ORM mapping)
    ↓
PostgreSQL Database
    ↓
Response Model (format output)
    ↓
JSON Response to Client
```

### Ví dụ chi tiết cho POST /employees/

1. **Request validation**: FastAPI kiểm tra Content-Type, method
2. **Schema validation**: Pydantic validate email format, required fields
3. **Business validation**: Kiểm tra email đã tồn tại chưa
4. **Database operation**: Insert vào bảng employees
5. **Response formatting**: Convert SQLAlchemy model → Pydantic response

## 4. Ví dụ Minh họa Request/Response

### 4.1 API Tạo nhân viên mới

**Request:**

```http
POST /employees/
Content-Type: application/json

{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@company.com",
  "position": "Backend Developer",
  "department": "Engineering",
  "start_date": "2024-01-15"
}
```

**Response (Success - 200):**

```json
{
  "id": 1,
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@company.com",
  "position": "Backend Developer",
  "department": "Engineering",
  "start_date": "2024-01-15"
}
```

**Response (Error - 400):**

```json
{
  "detail": "Email already registered"
}
```

### 4.2 API Lấy danh sách nhân viên

**Request:**

```http
GET /employees/?department=Engineering&limit=5&offset=0&start_date_after=2024-01-01
```

**Response:**

```json
{
  "employees": [
    {
      "id": 1,
      "name": "Nguyễn Văn A",
      "email": "nguyenvana@company.com",
      "position": "Backend Developer",
      "department": "Engineering",
      "start_date": "2024-01-15"
    }
  ],
  "total": 1,
  "limit": 5,
  "offset": 0
}
```

### 4.3 API Cập nhật ca làm việc

**Request:**

```http
POST /workshifts/
Content-Type: application/json

{
  "employee_id": 1,
  "work_day": "2024-02-15",
  "shift": "full_day"
}
```

**Response (Create new):**

```json
{
  "status": "created",
  "work_shift": {
    "id": 1,
    "employee_id": 1,
    "work_day": "2024-02-15",
    "shift": "full_day"
  }
}
```

**Response (Update existing):**

```json
{
  "status": "updated",
  "work_shift": {
    "id": 1,
    "employee_id": 1,
    "work_day": "2024-02-15",
    "shift": "morning"
  }
}
```

## 5. Tư duy Backend và Best Practices

### 5.1 Separation of Concerns

- **Models**: Định nghĩa cấu trúc dữ liệu
- **Schemas**: Validation input/output
- **CRUD**: Logic thao tác database
- **Routers**: HTTP endpoints và error handling

### 5.2 Error Handling Strategy

```python
# Validation errors → 422 (Pydantic auto)
# Business logic errors → 400 (Manual HTTPException)
# Not found errors → 404
# Server errors → 500 (FastAPI auto)
```

### 5.3 Database Design Principles

- **Normalization**: Tách bảng để tránh duplicate data
- **Indexing**: Index trên các trường thường query (email, employee_id)
- **Constraints**: Foreign keys đảm bảo referential integrity

### 5.4 API Design Principles

- **RESTful**: Sử dụng HTTP methods đúng nghĩa
- **Consistent**: Response format nhất quán
- **Descriptive**: Error messages rõ ràng
- **Pagination**: Hỗ trợ phân trang cho large datasets

## 6. Kết luận

Hệ thống được thiết kế theo **kiến trúc layered** với các tầng rõ ràng:

- **Presentation Layer**: FastAPI routers
- **Business Layer**: CRUD operations
- **Data Layer**: SQLAlchemy models + PostgreSQL

Điều này đảm bảo:

- **Maintainability**: Dễ bảo trì và mở rộng
- **Testability**: Có thể test từng layer độc lập
- **Scalability**: Dễ dàng scale horizontal/vertical
- **Security**: Validation nhiều lớp, SQL injection protection
