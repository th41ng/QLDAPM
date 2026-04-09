# Mô Tả Các Bảng Dữ Liệu - Job Portal

Tài liệu này mô tả mục đích, vai trò và quan hệ chính của từng bảng trong cơ sở dữ liệu `job_portal`.

## 1. `users`

**Mục đích:** Lưu thông tin tài khoản đăng nhập của toàn hệ thống.

**Vai trò:**
- Quản lý 3 vai trò chính: `admin`, `recruiter`, `candidate`
- Là bảng gốc cho toàn bộ người dùng của hệ thống

**Dữ liệu chính:**
- Họ tên
- Email
- Mật khẩu đã mã hóa
- Vai trò
- Trạng thái tài khoản
- Hình thức đăng nhập ưu tiên
- Xác thực email

**Quan hệ:**
- 1 user có thể có 1 `company` nếu là recruiter
- 1 user có thể có 1 `candidate_profile` nếu là candidate
- 1 user có thể có nhiều `resumes`, `applications`, `otp_codes`, `audit_logs`

---

## 2. `companies`

**Mục đích:** Lưu thông tin doanh nghiệp của nhà tuyển dụng.

**Vai trò:**
- Dùng cho recruiter để quản lý hồ sơ công ty
- Hiển thị logo, website, địa chỉ, mô tả công ty trên dashboard và landing page

**Dữ liệu chính:**
- Tên công ty
- Mã số thuế
- Website
- Địa chỉ
- Mô tả
- Logo
- Lĩnh vực/industry

**Quan hệ:**
- Mỗi company thuộc về đúng 1 recruiter
- 1 company có thể có nhiều `job_postings`

---

## 3. `candidate_profiles`

**Mục đích:** Lưu hồ sơ sơ yếu lý lịch cơ bản của ứng viên.

**Vai trò:**
- Dùng để tạo CV online
- Dùng để hiển thị thông tin ứng viên trên hệ thống
- Hỗ trợ ứng tuyển và sàng lọc hồ sơ

**Dữ liệu chính:**
- Ngày sinh
- Giới tính
- Địa chỉ
- Tiêu đề hồ sơ
- Mô tả ngắn
- Chức danh hiện tại
- Số năm kinh nghiệm
- Mức lương mong muốn
- Địa điểm mong muốn
- Học vấn
- Kinh nghiệm
- Portfolio

**Quan hệ:**
- Mỗi candidate chỉ có 1 profile chính
- Profile thuộc về 1 `user`

---

## 4. `categories`

**Mục đích:** Lưu các nhóm phân loại lớn cho tag.

**Vai trò:**
- Là bảng cha của tag
- Dùng để gom tag theo nhóm như:
  - Ngành nghề
  - Kỹ năng
  - Kinh nghiệm
  - Địa điểm
  - Hình thức

**Dữ liệu chính:**
- Tên nhóm
- Slug
- Mô tả
- Trạng thái hoạt động

**Quan hệ:**
- 1 category có nhiều `tags`

---

## 5. `tags`

**Mục đích:** Lưu các tag chi tiết để lọc, tìm kiếm và gắn nhãn cho job/resume.

**Vai trò:**
- Lọc tin tuyển dụng theo kỹ năng, ngành nghề, địa điểm, kinh nghiệm
- Gắn tag cho CV để phục vụ matching
- Hỗ trợ tìm kiếm và sàng lọc CV/job

**Dữ liệu chính:**
- Tên tag
- Slug
- `category_id`
- Mô tả
- Trạng thái hoạt động

**Quan hệ:**
- Mỗi tag thuộc 1 `category`
- Tag được dùng trong `job_tags` và `resume_tags`

---

## 6. `job_postings`

**Mục đích:** Lưu các tin tuyển dụng do recruiter đăng.

**Vai trò:**
- Là bảng trung tâm của toàn bộ hệ thống tuyển dụng
- Cung cấp dữ liệu cho landing page, recruiter dashboard, trang job detail

**Dữ liệu chính:**
- Tiêu đề job
- Slug
- Mô tả ngắn
- Mô tả chi tiết
- Yêu cầu
- Trách nhiệm
- Địa điểm
- Hình thức làm việc
- Loại việc
- Cấp bậc kinh nghiệm
- Mức lương
- Số lượng tuyển
- Hạn nộp
- Trạng thái
- Cờ nổi bật

**Quan hệ:**
- Thuộc về 1 recruiter
- Thuộc về 1 company
- Có nhiều `tags` qua bảng `job_tags`
- Có nhiều `applications`

---

## 7. `resumes`

**Mục đích:** Lưu các bản CV của ứng viên.

**Vai trò:**
- Hỗ trợ tạo CV online
- Hỗ trợ upload CV file
- Là dữ liệu đầu vào cho ứng tuyển và sàng lọc

**Dữ liệu chính:**
- Tiêu đề CV
- Nguồn tạo (`manual` hoặc `upload`)
- Tên template
- Tên file gốc
- Đường dẫn file lưu
- Loại file
- MIME type
- Nội dung text trích xuất
- JSON dữ liệu có cấu trúc
- File PDF/DOCX được sinh ra
- Cờ CV chính

**Quan hệ:**
- Thuộc về 1 user ứng viên
- Có nhiều `tags` qua bảng `resume_tags`
- Được dùng trong `applications`
- Được dùng trong `match_scores`

---

## 8. `cv_templates`

**Mục đích:** Lưu các mẫu CV có sẵn để ứng viên chọn.

**Vai trò:**
- Tạo số liệu CV mẫu trên landing page
- Cung cấp template cho chức năng tạo CV

**Dữ liệu chính:**
- Tên mẫu
- Slug
- Mô tả ngắn
- Mô tả chi tiết
- Ảnh thumbnail
- Ảnh preview
- Định dạng hỗ trợ
- Trạng thái hoạt động

**Quan hệ:**
- Bảng độc lập, chủ yếu phục vụ giao diện CV

---

## 9. `job_tags`

**Mục đích:** Bảng liên kết nhiều-nhiều giữa job và tag.

**Vai trò:**
- Một job có thể gắn nhiều tag
- Một tag có thể xuất hiện ở nhiều job

**Quan hệ:**
- `job_id` tham chiếu `job_postings`
- `tag_id` tham chiếu `tags`

---

## 10. `resume_tags`

**Mục đích:** Bảng liên kết nhiều-nhiều giữa resume và tag.

**Vai trò:**
- Một CV có thể gắn nhiều tag
- Dùng cho lọc và matching hồ sơ ứng viên

**Quan hệ:**
- `resume_id` tham chiếu `resumes`
- `tag_id` tham chiếu `tags`

---

## 11. `applications`

**Mục đích:** Lưu lịch sử ứng tuyển của ứng viên vào job.

**Vai trò:**
- Theo dõi ứng viên đã nộp hồ sơ nào
- Cho recruiter duyệt, từ chối hoặc phỏng vấn

**Dữ liệu chính:**
- Ứng viên
- Job
- Resume được dùng khi ứng tuyển
- Thư xin việc
- Trạng thái hồ sơ
- Ghi chú recruiter
- Thời gian ứng tuyển

**Quan hệ:**
- Thuộc về 1 candidate
- Thuộc về 1 job
- Dùng 1 resume cụ thể

---

## 12. `otp_codes`

**Mục đích:** Lưu OTP dùng cho đăng nhập và đăng ký qua email.

**Vai trò:**
- Gửi OTP qua Gmail App Password
- Xác thực login/register không cần mật khẩu trong một số luồng

**Dữ liệu chính:**
- Email
- Vai trò
- Mục đích OTP: `register`, `login`, `reset`
- Mã OTP đã hash
- Thời gian hết hạn
- Thời gian có thể gửi lại
- Số lần thử
- Payload tạm cho register
- IP yêu cầu

**Quan hệ:**
- Có thể liên kết với `users`
- Dùng tạm thời, OTP hết hạn sẽ bị xóa hoặc vô hiệu hóa

---

## 13. `match_scores`

**Mục đích:** Lưu điểm matching giữa CV và job.

**Vai trò:**
- Phục vụ sàng lọc CV
- Hỗ trợ chấm điểm phù hợp giữa ứng viên và tin tuyển dụng

**Dữ liệu chính:**
- Job
- Resume
- Candidate
- Điểm số
- Breakdown chi tiết theo tiêu chí

**Quan hệ:**
- Thuộc về `job_postings`
- Thuộc về `resumes`
- Thuộc về `users`

---

## 14. `audit_logs`

**Mục đích:** Ghi lịch sử thao tác hệ thống.

**Vai trò:**
- Theo dõi hành động của admin hoặc hệ thống
- Hữu ích cho kiểm tra và quản trị

**Dữ liệu chính:**
- Người thực hiện
- Hành động
- Loại đối tượng
- ID đối tượng
- Dữ liệu trước và sau khi thay đổi
- Địa chỉ IP

**Quan hệ:**
- Thuộc về 1 `user`

---

## Tổng kết vai trò của hệ thống bảng

### Nhóm tài khoản
- `users`
- `candidate_profiles`
- `companies`

### Nhóm tuyển dụng
- `job_postings`
- `applications`
- `match_scores`

### Nhóm phân loại và tìm kiếm
- `categories`
- `tags`
- `job_tags`
- `resume_tags`

### Nhóm CV
- `resumes`
- `cv_templates`

### Nhóm bảo mật và quản trị
- `otp_codes`
- `audit_logs`

Tài liệu này có thể dùng làm phần mô tả cơ sở dữ liệu trong báo cáo đồ án hoặc làm tài liệu tham khảo khi chỉnh sửa schema về sau.
