Bạn là một lập trình viên backend chuyên nghiệp.  
Hãy giúp tôi xây dựng một project backend sử dụng **Python 3.10+, FastAPI, SQLAlchemy, PostgreSQL** để giải quyết 3 yêu cầu sau:

### 1. Yêu cầu hệ thống
- Sử dụng **FastAPI** để xây dựng API.
- Sử dụng **SQLAlchemy ORM** để kết nối PostgreSQL.
- Tổ chức project theo cấu trúc module: `app/main.py`, `app/models.py`, `app/schemas.py`, `app/database.py`, `app/crud.py`, `app/routers/...`.
- Có file `requirements.txt` liệt kê dependencies (fastapi, uvicorn, psycopg2, sqlalchemy, pydantic).
- Sử dụng **Pydantic schemas** để validate request/response.
- Code sạch, dễ mở rộng, có chú thích.

### 2. Bài tập cần triển khai

#### Bài 1: API tạo nhân viên mới
- Endpoint: `POST /employees/`
- Input: `name` (str, bắt buộc), `email` (str, bắt buộc, unique), `position` (str), `department` (str), `start_date` (date).
- Validate email không trùng.
- Lưu vào DB, trả về JSON thông tin nhân viên đã tạo.

#### Bài 2: API lấy danh sách nhân viên theo phòng ban
- Endpoint: `GET /employees/`
- Query params: `department` (optional).
- Trả về danh sách nhân viên (JSON).
- Yêu cầu nâng cao: hỗ trợ `limit`, `offset` (pagination) và filter nâng cao: `start_date_after` (date).

#### Bài 3: API cập nhật ca làm việc cho nhân viên
- Endpoint: `POST /workshifts/`
- Input: `employee_id` (int), `work_day` (date, format YYYY-MM-DD), `shift` (enum: morning, afternoon, full_day).
- Nếu đã có lịch trong ngày => update shift.
- Nếu chưa có => insert mới.
- Output: JSON thông báo "updated" hoặc "created".

### 3. Database schema gợi ý
- Table `employees`: id (PK), name, email (unique), position, department, start_date.
- Table `work_shifts`: id (PK), employee_id (FK), work_day, shift.

### 4. Kết quả mong muốn
- Sinh ra code đầy đủ cho toàn bộ project FastAPI (có thể chạy trực tiếp sau khi `pip install -r requirements.txt` và cấu hình DB).
- Có file migration mẫu (hoặc hướng dẫn tạo DB với SQLAlchemy).
- Có ví dụ request/response JSON cho từng API.
- Viết code rõ ràng, dễ đọc, tuân thủ best practice.
