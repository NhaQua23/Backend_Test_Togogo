# Employee Management System

A FastAPI backend application for managing employees and work shifts using PostgreSQL database.

## Features

- **Employee Management**: Create and list employees with filtering and pagination
- **Work Shift Management**: Create and update work shifts for employees
- **Data Validation**: Pydantic schemas for request/response validation
- **Database Integration**: SQLAlchemy ORM with PostgreSQL
- **API Documentation**: Auto-generated OpenAPI docs

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Project Structure

```
Backend_Intern/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # Database operations
│   └── routers/
│       ├── __init__.py
│       ├── employees.py # Employee endpoints
│       └── workshifts.py # Work shift endpoints
├── requirements.txt     # Dependencies
├── create_db.py        # Database setup script
└── README.md           # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

Make sure PostgreSQL is running and create a database:

```sql
CREATE DATABASE employee_db;
```

### 3. Configure Database Connection

Set the database URL environment variable (optional):

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/employee_db"
```

Default connection: `postgresql://postgres:password@localhost:5432/employee_db`

### 4. Create Database Tables

```bash
python create_db.py
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Employee

**POST** `/employees/`

Create a new employee with unique email validation.

**Request Body:**

```json
{
  "name": "John Doe",
  "email": "john.doe@company.com",
  "position": "Software Engineer",
  "department": "Engineering",
  "start_date": "2024-01-15"
}
```

**Response:**

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@company.com",
  "position": "Software Engineer",
  "department": "Engineering",
  "start_date": "2024-01-15"
}
```

### 2. Get Employees

**GET** `/employees/`

Get list of employees with optional filtering and pagination.

**Query Parameters:**

- `department` (optional): Filter by department
- `start_date_after` (optional): Filter employees who started after this date
- `limit` (optional): Number of employees to return (1-1000, default: 100)
- `offset` (optional): Number of employees to skip (default: 0)

**Example Request:**

```
GET /employees/?department=Engineering&limit=10&offset=0
```

**Response:**

```json
{
  "employees": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@company.com",
      "position": "Software Engineer",
      "department": "Engineering",
      "start_date": "2024-01-15"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

### 3. Create/Update Work Shift

**POST** `/workshifts/`

Create or update work shift for an employee. If a shift already exists for the date, it will be updated.

**Request Body:**

```json
{
  "employee_id": 1,
  "work_day": "2024-01-20",
  "shift": "full_day"
}
```

**Shift Types:**

- `morning`
- `afternoon`
- `full_day`

**Response:**

```json
{
  "status": "created",
  "work_shift": {
    "id": 1,
    "employee_id": 1,
    "work_day": "2024-01-20",
    "shift": "full_day"
  }
}
```

## Example Usage with curl

### Create Employee

```bash
curl -X POST "http://localhost:8000/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane.smith@company.com",
    "position": "Product Manager",
    "department": "Product",
    "start_date": "2024-02-01"
  }'
```

### Get Employees by Department

```bash
curl "http://localhost:8000/employees/?department=Product&limit=5"
```

### Create Work Shift

```bash
curl -X POST "http://localhost:8000/workshifts/" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "work_day": "2024-02-15",
    "shift": "morning"
  }'
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (e.g., email already exists)
- `404`: Not Found (e.g., employee not found)
- `422`: Validation Error (e.g., invalid email format)

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Schema

**employees** table:

- `id`: Primary key (integer)
- `name`: Employee name (string, required)
- `email`: Employee email (string, unique, required)
- `position`: Job position (string, optional)
- `department`: Department (string, optional)
- `start_date`: Start date (date, optional)

**work_shifts** table:

- `id`: Primary key (integer)
- `employee_id`: Foreign key to employees (integer, required)
- `work_day`: Work date (date, required)
- `shift`: Shift type enum (morning/afternoon/full_day, required)
