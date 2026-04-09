# Phân Tích Hệ Thống Thông Tin Tuyển Dụng (Job Portal)

## 📋 TỔNG QUAN HỆ THỐNG

### 1. Mục Đích & Chức Năng Chính
Hệ thống cổng thông tin tuyển dụng là nền tảng kết nối người tìm việc (Candidate) với nhà tuyển dụng (Recruiter) thông qua 3 vai trò chính:

- **Admin**: Quản lý toàn hệ thống, duyệt content, quản lý categories/tags
- **Recruiter**: Đăng tin tuyển dụng, xem CV candidates, quản lý hồ sơ ứng tuyển
- **Candidate**: Tạo CV, tìm việc, ứng tuyển, quản lý hồ sơ cá nhân

---

## 🏗️ KIẾN TRÚC DỮ LIỆU

### A. Entities Chính (13 class)

#### 1. **User** (Người Dùng)
- Lưu thông tin tài khoản và xác thực
- **Vai trò:** Là bảng gốc của toàn hệ thống
- **Quan hệ:**
  - 1 User → 0..1 Company (nếu recruiter)
  - 1 User → 0..1 CandidateProfile (nếu candidate)
  - 1 User → * Resume
  - 1 User → * JobPosting (nếu recruiter)
  - 1 User → * Application (nếu candidate)

#### 2. **Company** (Công Ty)
- Thông tin doanh nghiệp của recruiter
- **Thuộc tính chính:** Tên, tax code, website, address, logo, industry
- **Quan hệ:** 1 company → * JobPosting

#### 3. **CandidateProfile** (Hồ Sơ Ứng Viên)
- Thông tin cơ bản của candidate
- **Thuộc tính:** DOB, gender, headline, summary, current position, experience, education
- **Quan hệ:** 1-to-1 với User

#### 4. **Resume** (CV/Bản Sơ Yếu Lý Lịch)
- Lưu CV dưới nhiều định dạng
- **Source Types:**
  - `manual`: Tạo từ template online
  - `upload`: Upload file CV
- **Lưu trữ:**
  - `raw_text`: Nội dung text trích xuất
  - `structured_json`: Dữ liệu có cấu trúc (education, experience, skills)
  - `generated_pdf_path`: File PDF sinh ra
  - `generated_docx_path`: File DOCX sinh ra
- **Đặc biệt:** `is_primary` đánh dấu CV chính

#### 5. **JobPosting** (Tin Tuyển Dụng)
- Tin tuyển dụng do recruiter đăng
- **Thuộc tính chính:**
  - Tiêu đề, slug, mô tả, yêu cầu, trách nhiệm
  - `workplace_type`: onsite, hybrid, remote
  - `employment_type`: full-time, part-time, contract, internship
  - `experience_level`: intern, fresher, junior, middle, senior, lead
  - `salary_min`, `salary_max`, `salary_currency`
  - `vacancy_count`: Số lượng tuyển nhân sự
  - `deadline`: Hạn nộp hồ sơ
  - `status`: draft, published, closed
  - `is_featured`: Cờ nổi bật
- **Quan hệ:** 1 job → * Application, * MatchScore, * Tags (many-to-many)

#### 6. **Application** (Hồ Sơ Ứng Tuyển)
- Ghi nhận khi candidate ứng tuyển
- **Workflow Status:**
  - `submitted`: Vừa được nộp
  - `reviewing`: Đang được xem xét
  - `interview`: Gọi phỏng vấn
  - `accepted`: Được chấp nhận
  - `rejected`: Bị từ chối
  - `withdrawn`: Rút lại hồ sơ
- **Unique Constraint:** (candidate_user_id, job_id) - 1 candidate chỉ ứng tuyển 1 lần per job

#### 7. **MatchScore** (Điểm Phù Hợp)
- Lưu kết quả matching giữa resume và job
- **Công thức:** So sánh tags (skills) của job vs resume
- **Lưu trữ:**
  - `score`: Điểm match (0-100)
  - `breakdown_json`: Chi tiết scoring breakdown

#### 8. **Category** (Nhóm Phân Loại)
- Nhóm lớn của tags
- **Ví dụ:** Kỹ năng, Ngành nghề, Địa điểm, Kinh nghiệm, Hình thức làm việc

#### 9. **Tag** (Thẻ Chi Tiết)
- Chi tiết tag trong mỗi category
- **Many-to-many với:**
  - JobPosting (qua job_tags): mô tả yêu cầu skill/ngành/vị trí
  - Resume (qua resume_tags): mô tả skill/kinh nghiệm của candidate

#### 10. **CvTemplate** (Mẫu CV)
- Các template CV có sẵn cho candidate chọn
- **Define:** Tên, slug, thumbnail, preview, file format supported

#### 11. **OtpCode** (Mã OTP)
- Lưu OTP cho đăng ký, đăng nhập, reset password
- **Purpose:** register, login, reset
- **Bảo mật:**
  - `code_hash`: Lưu hash (không plain text)
  - `max_attempts`: Tối đa 5 lần nhập sai
  - `expires_at`: Hết hạn sau 5 phút
  - `resend_available_at`: Có thể resend sau 60 phút
  - `request_ip`: Theo dõi IP request

#### 12. **AuditLog** (Nhật Ký Kiểm Trace)
- Ghi lại tất cả hành động thay đổi dữ liệu
- **Lưu trữ:**
  - `action`: Hành động (create, update, delete)
  - `entity_type`, `entity_id`: Loại và ID entity bị thay đổi
  - `before_json`, `after_json`: Dữ liệu trước/sau
  - `ip_address`: IP địa chỉ user
- **Dùng:** Compliance, security audit

---

## 🔗 MÔ HÌNH QUAN HỆ

### Cascade Delete (Xóa theo Tầng)
```
User deleted → Xóa: Company, CandidateProfile, Resume, JobPosting, Application
Company deleted → Xóa: JobPosting
JobPosting deleted → Xóa: Application, MatchScore
Resume deleted → Xóa: Application, MatchScore
```

### Many-to-Many Relationships
```
JobPosting ⟷ Tag (qua bảng job_tags)
Resume ⟷ Tag (qua bảng resume_tags)
```

---

## 💼 CÁC QUY TRÌNH NGHIỆP VỤ

### A. QUY TRÌNH ĐĂNG KÝ/ĐĂNG NHẬP

#### 1. Đăng Ký với OTP
```
1. User nhập email
2. System gửi OTP
   - Tạo OtpCode record
   - code_hash được mã hóa
   - expires_at = now + 5 mins
   - resend_available_at = now + 60 mins
3. User nhập OTP + thông tin (full_name, password, role)
4. System verify OTP
   - Kiểm tra attempts < max_attempts
   - Kiểm tra expires_at
   - Verify code_hash
5. Tạo User record
   - password_hash = scrypt hash
   - role = candidate/recruiter
   - status = active
   - email_verified = true
6. Nếu recruiter: Tạo Company record
   Nếu candidate: Tạo CandidateProfile record

#### 2. Đăng Nhập
- Phương pháp 1: email + password
- Phương pháp 2: email + OTP (truyền auth_method_preference)
```

### B. QUY TRÌNH RECRUITER ĐĂNG TIN

```
1. Recruiter tạo JobPosting
   - Nhập: title, description, requirements, salary, location, etc.
   - Gắn tags từ các categories (Kỹ năng, Ngành nghề, Vị trí)
   - status = "draft"
   - recruiter_user_id = current user
   - company_id = company của current recruiter

2. Vào bảng job_tags
   - Insert (job_id, tag_id) cho mỗi tag được chọn

3. Recruiter publish tin
   - Cập nhật status = "published"
   - Cập nhật published_at = now()

4. Quản lý ứng tuyển
   - Xem list Applications (status = submitted)
   - Review hồ sơ / Resume
   - Cập nhật Application status (reviewing, interview, accepted, rejected)
   - Thêm recruiter_note
```

### C. QUY TRÌNH CANDIDATE ỨNG TUYỂN

```
1. Candidate xem danh sách JobPosting
   - Filter theo tags (skills, location, experience_level, salary)
   - Xem chi tiết job (description, requirements, company info)

2. Candidate tạo CV
   Option A: Từ template
   - Chọn CvTemplate
   - Fill thông tin (education, experience, skills)
   - Gắn tags cho CV (via resume_tags)
   - Resume.source_type = "manual"
   - Generate PDF/DOCX từ structured_json
   
   Option B: Upload file
   - Upload file CV (PDF/DOCX)
   - Extract raw_text từ file
   - Parse structured_json (tùy chọn hoặc manual)
   - Resume.source_type = "upload"

3. Candidate ứng tuyển
   - Chọn JobPosting
   - Chọn Resume để nộp
   - Viết cover_letter (optional)
   - Tạo Application record
   - Application.status = "submitted"

4. System tính MatchScore
   - So sánh tags của JobPosting vs Resume
   - Tính score dựa trên:
     * Độ trùng khớp tags
     * Level matching (junior job vs senior resume, etc.)
     * Keyword matching trong description
   - Lưu MatchScore record

5. Candidate theo dõi hồ sơ
   - Xem Application status
   - Withdraw hồ sơ nếu muốn (status = "withdrawn")
```

### D. QUY TRÌNH HỆ THỐNG GỢI Ý

```
1. Widget Recommend Job trên landing page
   - Lấy top N jobs theo:
     * is_featured = true
     * status = published
     * deadline >= today
   - Order by created_at DESC hoặc match score DESC

2. Matching Algorithm
   - Input: Resume tags, JobPosting tags
   - Output: MatchScore (0-100)
   - Algorithm:
     * Count matched tags
     * Weighted scoring by tag category
     * Experience level alignment
     * Salary expectation vs job offer
   - Lưu breakdown_json chi tiết

3. Display Recommendation
   - Show jobs sorted by match score
   - Highlight high-match jobs (> 75%)
```

---

## 📊 FLOW DIAGRAMS

### Sequence: Candidate Ứng Tuyển
```
Candidate              Frontend           Backend            Database
   |                      |                  |                  |
   |--search jobs-------->|                  |                  |
   |                      |<-get jobs------->|--query job_tags--|
   |                      |<--------jobs-----|-tags matched---->|
   |                      |                  |                  |
   |--view job detail---->|                  |                  |
   |                      |<-show detail-----|                  |
   |                      |                  |                  |
   |--apply with CV------>|                  |                  |
   |                      |--create app----->|--insert app----->|
   |                      |                  |--calc match----->|
   |                      |<-app_id----------|<-match_score----|
   |                      |<-success---------|                  |
   |<-----confirm---------|                  |                  |
```

### Sequence: Recruiter Quản Lý Hồ Sơ
```
Recruiter              Frontend           Backend            Database
   |                      |                  |                  |
   |--login with OTP----->|                  |                  |
   |                      |--verify OTP----->|--check otp----->|
   |                      |<-success---------|<-create session-|
   |                      |                  |                  |
   |--view applications-->|                  |                  |
   |                      |<-list apps------>|--query for----->|
   |                      |                  |  recruiter_id    |
   |<-show apps----------|                  |<-app with status-|
   |                      |                  |                  |
   |--review resume------>|                  |                  |
   |                      |<-show resume---->|--get file----->|
   |                      |                  |<-file content----|
   |                      |                  |                  |
   |--update status------>|                  |                  |
   |                      |--update app----->|--update status-->|
   |                      |                  |--audit log------>|
   |<-success----------|  |<-confirmed------|<-return---------|
```

---

## 🔐 BẢNG TRẠNG THÁI (Enum Values)

### User.role
- `admin`: System administrator
- `recruiter`: Nhà tuyển dụng
- `candidate`: Ứng viên

### User.status
- `active`: Tài khoản hoạt động
- `locked`: Bị khóa (vượt max OTP attempts)
- `pending`: Chờ verify email

### User.auth_method_preference
- `password`: Đăng nhập bằng mật khẩu
- `otp`: Đăng nhập bằng OTP (không cần mật khẩu)

### JobPosting.status
- `draft`: Tin chưa đăng
- `published`: Đang tuyển dụng
- `closed`: Đã đóng tuyển

### JobPosting.workplace_type
- `onsite`: Làm việc tại văn phòng
- `hybrid`: Vừa tại văn phòng, vừa remote
- `remote`: Toàn bộ remote

### JobPosting.employment_type
- `full-time`: Toàn thời gian
- `part-time`: Bán thời gian
- `contract`: Hợp đồng
- `internship`: Thực tập

### JobPosting.experience_level
- `intern`: Thực tập sinh
- `fresher`: Mới tốt nghiệp
- `junior`: Junior (1-2 năm)
- `middle`: Middle (2-5 năm)
- `senior`: Senior (5+ năm)
- `lead`: Leadership

### Application.status
- `submitted`: Vừa nộp
- `reviewing`: Đang review
- `interview`: Gọi phỏng vấn
- `accepted`: Được nhận
- `rejected`: Bị từ chối
- `withdrawn`: Rút lại

### Resume.source_type
- `manual`: Tạo từ template
- `upload`: Upload file

### OtpCode.purpose
- `register`: Đăng ký tài khoản
- `login`: Đăng nhập
- `reset`: Reset password

---

## 🛡️ BẢNG CONSTRAINTS & INDEXES

### Unique Constraints
- `users.email`: Không trùng email
- `tags.name`, `tags.slug`: Tag không trùng
- `categories.name`, `categories.slug`: Categ không trùng
- `companies.recruiter_user_id`: 1 recruiter = 1 company
- `candidate_profiles.user_id`: 1 candidate = 1 profile
- `applications.(candidate_user_id, job_id)`: 1 candidate ứng tuyển 1 lần per job
- `resumes.id`: Primary key
- `job_postings.slug`: Slug tuyệt đối

### Foreign Keys (Cascade Delete)
- Company.recruiter_user_id → User.id
- CandidateProfile.user_id → User.id
- Tag.category_id → Category.id
- Resume.user_id → User.id
- JobPosting.recruiter_user_id → User.id
- JobPosting.company_id → Company.id
- Application.candidate_user_id → User.id
- Application.job_id → JobPosting.id
- Application.resume_id → Resume.id
- MatchScore.job_id → JobPosting.id
- MatchScore.resume_id → Resume.id
- MatchScore.candidate_user_id → User.id
- OtpCode.user_id → User.id (SET NULL)
- AuditLog.actor_user_id → User.id

### Indexes
- `users(role, status)`
- `job_postings(status, location, experience_level)`
- `resumes(user_id, is_primary)`
- `tags(category_id, is_active)`
- `otp_codes(email, purpose, request_ip)`
- `applications(status)`

---

## 📈 VÍ DỤ DỮ LIỆU SẼ LƯU

### User Candidate
```json
{
  "id": 3,
  "full_name": "Tien Candidate",
  "email": "dinhtien09102004@gmail.com",
  "password_hash": "scrypt:...",
  "role": "candidate",
  "auth_method_preference": "otp",
  "status": "active",
  "email_verified": true,
  "phone": "0900000003",
  "created_at": "2024-01-01 10:00:00"
}
```

### CandidateProfile
```json
{
  "id": 1,
  "user_id": 3,
  "dob": "2004-10-09",
  "gender": "Male",
  "address": "TP Ho Chi Minh",
  "headline": "Python Developer",
  "summary": "Passionate about web development",
  "current_title": "Junior Python Developer",
  "years_experience": 1,
  "expected_salary": "10-15M VND",
  "desired_location": "TP Ho Chi Minh, Da Nang"
}
```

### Resume (from Template)
```json
{
  "id": 1,
  "user_id": 3,
  "title": "CV Python Developer - 2024",
  "source_type": "manual",
  "template_name": "professional-blue",
  "raw_text": "TIEN CANDIDATE...",
  "structured_json": {
    "education": [
      {
        "school": "OU University",
        "degree": "Bachelor",
        "field": "Information Technology",
        "start": "2022",
        "end": "2026"
      }
    ],
    "experience": [
      {
        "company": "MyApp Web",
        "position": "Intern",
        "start": "2023-06",
        "end": "2024-01"
      }
    ],
    "skills": ["Python", "Flask", "ReactJS", "MySQL"]
  },
  "generated_pdf_path": "/storage/resumes/resume_1.pdf",
  "is_primary": true
}
```

### JobPosting
```json
{
  "id": 1,
  "recruiter_user_id": 2,
  "company_id": 1,
  "title": "Python Backend Developer",
  "slug": "python-backend-developer-myappweb",
  "description": "...",
  "requirements": "...",
  "location": "TP Ho Chi Minh",
  "workplace_type": "hybrid",
  "employment_type": "full-time",
  "experience_level": "junior",
  "salary_min": 12000000,
  "salary_max": 18000000,
  "salary_currency": "VND",
  "vacancy_count": 2,
  "deadline": "2024-12-31",
  "status": "published",
  "is_featured": true
}
```

### Application
```json
{
  "id": 1,
  "candidate_user_id": 3,
  "job_id": 1,
  "resume_id": 1,
  "cover_letter": "I am very interested...",
  "status": "submitted",
  "applied_at": "2024-12-01 14:30:00"
}
```

### MatchScore
```json
{
  "id": 1,
  "job_id": 1,
  "resume_id": 1,
  "candidate_user_id": 3,
  "score": 82.5,
  "breakdown_json": {
    "skill_match": 85,
    "experience_match": 70,
    "location_match": 100,
    "salary_match": 80,
    "weights": {
      "skill": 0.4,
      "experience": 0.3,
      "location": 0.2,
      "salary": 0.1
    }
  }
}
```

---

## ⚙️ BUSINESS LOGIC & SERVICES

### 1. OTP Service
- Send OTP: Tạo code, hash, gửi email, lưu DB
- Verify OTP: Check code, expiry, attempts, use OTP
- Resend OTP: Check resend timeout, tạo code mới

### 2. Matching Service
- Calculate Match Score: So sánh tags, experience, location, salary
- Get Job Recommendations: Top N jobs by match score
- Get Candidate Recommendations: Top N candidates per job

### 3. CV Service
- Generate PDF/DOCX from template
- Extract text từ uploaded file
- Parse CV structure (education, experience, skills)
- Validate CV data

### 4. Mail Service
- Send OTP email
- Send application status notification
- Send interview invitation

### 5. Storage Service
- Upload CV file
- Store PDF/DOCX generated
- Manage file paths, mime types

### 6. Audit Service
- Log user actions
- Store before/after JSON
- Track IP address
- Generate audit reports

---

## 🎯 SUMMARY - NGHIỆP VỤ ĐÃ LÀM

| # | Functionality | Implementation | Status |
|---|---------------|-----------------|--------|
| 1 | User Registration & Login | OTP + Password auth, 3 roles | ✅ |
| 2 | Candidate Profile Management | Full profile with experience, education | ✅ |
| 3 | CV Creation & Management | Manual templates + Upload files | ✅ |
| 4 | Job Posting Management | Create, publish, edit, close jobs | ✅ |
| 5 | Job Application | Submit resume, cover letter, track status | ✅ |
| 6 | Application Workflow | Status: submitted→reviewing→interview→result | ✅ |
| 7 | Tag/Category System | Hierarchical categorization, flexible filtering | ✅ |
| 8 | Job-Resume Matching | Automatic score calculation, recommendations | ✅ |
| 9 | Company Profile | Recruiter company info, logo, industry | ✅ |
| 10 | Security & Audit | OTP validation, audit logs, IP tracking | ✅ |
| 11 | Email Notifications | OTP, application updates, interview invites | ✅ |
| 12 | File Management | CV upload, store, generate PDF/DOCX | ✅ |

---

## 🔧 TECH STACK

- **Backend:** Flask (Python)
- **Frontend:** React JS
- **Database:** MySQL with SQLAlchemy ORM
- **Storage:** File system (PDF, DOCX, original files)
- **Authentication:** Email/Password, OTP via email
- **Security:** Scrypt password hashing, OTP code hashing
- **APIs:** RESTful JSON APIs

---

## 📝 GHI CHÚ QUAN TRỌNG

1. **Unique Candidate-Job Application**: Mỗi candidate chỉ ứng tuyển 1 lần per job
2. **Cascade Relationships**: Xóa parent tự động xóa children
3. **JSON Flexibility**: Sử dụng JSON cho flexible data (structured_json, breakdown_json)
4. **Tag System**: Dùng để filter, recommend, match
5. **Audit Trail**: Ghi lại mọi thay đổi dữ liệu
6. **OTP Security**: Code hash, max attempts, expiration
