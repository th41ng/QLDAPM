# Hệ thống cổng thông tin việc làm

Project tách thành 2 phần:

- `frontend/`: React JS web cho ứng viên và nhà tuyển dụng
- `backend/`: Flask web template cho admin

## Chức năng chính

1. Tạo và quản lý CV online
2. Tìm kiếm và lọc tin tuyển dụng
3. Nộp hồ sơ ứng tuyển theo từng CV
4. Đăng tin tuyển dụng mới
5. Quản lý hồ sơ ứng tuyển
6. Sàng lọc CV tự động và gợi ý việc làm
7. Đăng ký và đăng nhập bằng `email + password` hoặc `email + OTP`

## Cài đặt nhanh

### 1. Cài thư viện Python
python -m venv venv
venv\Scripts\activate
```bash
pip install -r requirements.txt
```

### 2. Tạo database MySQL

- Mở MySQL Workbench
- Mở file `schema.sql`
- Chạy toàn bộ script để tạo database, user MySQL riêng và dữ liệu mẫu

### 3. Kiểm tra file `.env`

File `.env` đã có sẵn ở thư mục gốc.
Nếu MySQL của bạn khác cấu hình hiện tại thì sửa lại `DATABASE_URL` cho đúng.

### 4. Chạy backend Flask admin

Từ thư mục gốc `C:\\HeThongCongThongTin`:

```bash
python backend/run.py
```

Backend chạy ở:

```text
http://127.0.0.1:5001
```

### 5. Chạy frontend React

Từ thư mục gốc:

```bash
cd frontend
npm install
npm run dev
```

Frontend chạy ở:

```text
http://127.0.0.1:5173
```

## MySQL

File `schema.sql` đã gồm:

- Tạo database `job_portal`
- Tạo user MySQL riêng `jobportal_user`
- Tạo đủ bảng cho `users`, `companies`, `candidate_profiles`, `categories`, `tags`, `job_postings`, `resumes`, `applications`, `otp_codes`, `match_scores`, `audit_logs`
- `categories` là bảng nhóm tag, `tags` là bảng tag chi tiết với khóa ngoại `category_id`
- Có dữ liệu seed cho 3 tài khoản mẫu

Tài khoản seed:

- Admin: `myappweb145@gmail.com`
- Recruiter: `2251012132tien@ou.edu.vn`
- Candidate: `dinhtien09102004@gmail.com`
- Mật khẩu chung: `123456`

## Frontend React

Frontend React có các trang:

- Trang chủ
- Trang tin tuyển dụng
- Trang chi tiết việc làm
- Trang đăng nhập / đăng ký
- Trang tạo hồ sơ ứng viên
- Trang xem hồ sơ đã tạo
- Trang mẫu CV
- Trang tuyển dụng cho recruiter

## Backend Flask

Backend Flask giữ giao diện admin:

- Dashboard thống kê
- CRUD categories
- CRUD người dùng
- CRUD tin tuyển dụng
- CRUD hồ sơ ứng tuyển
- CRUD tags
- Khóa / mở khóa tài khoản

## Cấu hình `.env`

Chỉ cần file `.env` ở thư mục gốc. Project không dùng `.env.example`.

Các biến quan trọng:

- `DATABASE_URL=mysql+pymysql://jobportal_user:JobPortal123%21@127.0.0.1:3306/job_portal`
- `MAIL_USERNAME=myappweb145@gmail.com`
- `MAIL_PASSWORD=cooa sagg ebvo jlgj`
- `CLOUDINARY_CLOUD_NAME=dqukehyry`
- `CLOUDINARY_API_KEY=375756179188283`
- `CLOUDINARY_API_SECRET=...`
- `OTP_EXPIRES_MINUTES=5`
- `OTP_RESEND_SECONDS=60`
- `OTP_MAX_ATTEMPTS=5`
- `OTP_MAX_SENDS_PER_HOUR=5`
- `FRONTEND_URL=http://127.0.0.1:5173`

Lưu ý:

- Project hiện dùng MySQL làm database mặc định.
- Không còn fallback SQLite cho backend nữa.

Public API cho trang chủ và auth:

- `GET /api/tags/categories`
- `GET /api/tags?category=industry`
- `GET /api/tags`
- `POST /api/auth/otp/send`
- `POST /api/auth/otp/verify`
- `POST /api/auth/otp/resend`

Luồng OTP:

- `Đăng nhập bằng OTP`: nhập email -> gửi OTP qua Gmail App Password -> nhập OTP -> xác thực và nhận token
- `Đăng ký bằng OTP`: nhập họ tên, email, mật khẩu, role -> gửi OTP -> nhập OTP -> tạo tài khoản và đăng nhập

Logo công ty và ảnh đại diện có thể upload từ API và sẽ được lưu trên Cloudinary, còn URL lưu trong MySQL.

## Ghi chú

- Frontend React đang kết nối API theo REST
- Backend Flask chia theo nhóm chức năng để file không quá dài
- Nên import `schema.sql` trước khi chạy backend lần đầu
