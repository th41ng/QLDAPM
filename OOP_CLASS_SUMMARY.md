# OOP Class Diagram - Hệ Thống Thông Tin Tuyển Dụng

## 📊 TỔNG HỢP THIẾT KẾ OOP

Tôi đã vẽ lại sơ đồ lớp theo **hướng OOP (Object-Oriented Programming)** với các đặc điểm chính:

---

## ✨ ĐIỂM NỔIBẬT CỦa THIẾT KẾ OOP

### 1️⃣ **3 Base Abstract Classes** (Kế Thừa)
- **BaseModel** ← 13 Entity classes
- **BaseService** ← 8 Service classes  
- **BaseRepository** ← 11 Repository classes

### 2️⃣ **8 Business Services** (Tầng Logic)
- `AuthenticationService` - Xác thực người dùng
- `OtpService` - Quản lý OTP
- `ResumeService` - Quản lý CV
- `JobService` - Quản lý tin tuyển dụng
- `ApplicationService` - Quản lý hồ sơ ứng tuyển
- `MatchingService` - Tính điểm phù hợp
- `MailService` - Gửi email
- `StorageService` - Lưu trữ file

### 3️⃣ **11 Repositories** (Tầng Dữ Liệu)
- `UserRepository`, `CompanyRepository`, `ResumeRepository`
- `JobPostingRepository`, `ApplicationRepository`, `MatchScoreRepository`
- `TagRepository`, `CategoryRepository`, `OtpCodeRepository`
- `AuditLogRepository`, `CvTemplateRepository`

### 4️⃣ **13 Entity Models** (Tầng Dữ Liệu)
- Core: User, Company, CandidateProfile
- Content: Resume, JobPosting, Application
- Tags: Category, Tag, CvTemplate
- Matching: MatchScore
- Security: OtpCode, AuditLog

---

## 🏗️ LỚP TỰC TƯỢNG (Abstract Classes)

### BaseModel
```
Properties:
  - id: int (PK)
  - created_at: datetime
  - updated_at: datetime

Methods:
  + save(): void
  + delete(): void
  + to_dict(): dict
  + get_id(): int
```

### BaseService (ABC)
```
Properties:
  - db_session: Session

Methods:
  + execute(): any (abstract)
  + validate(): bool (abstract)
  + handle_error(): void
```

### BaseRepository (ABC)
```
Properties:
  - model: class
  - db: Session

Methods:
  + find_by_id(id): T
  + find_all(): List[T]
  + create(data): T
  + update(id, data): T
  + delete(id): bool
```

---

## 🔗 KIẾN TRÚC PHÂN TẦNG (Layered Architecture)

```
Presentation Layer
       ↓ HTTP REST
Application Layer (Controllers/Routes)
       ↓ Dependency Injection
Service Layer (Business Logic)
  ├─ AuthenticationService
  ├─ ResumeService
  ├─ JobService
  ├─ ApplicationService
  ├─ MatchingService
  └─ ...
       ↓ Method Calls
Data Access Layer (Repositories)
  ├─ UserRepository
  ├─ ResumeRepository
  ├─ JobPostingRepository
  └─ ...
       ↓ ORM
Model Layer (Entities)
  ├─ User
  ├─ Resume
  ├─ JobPosting
  └─ ...
       ↓ SQL
Database Layer (MySQL)
```

---

## 📐 OOP PRINCIPLES APPLIED

### ✅ **1. Inheritance (Kế Thừa)**
```
BaseModel
  ├─ User
  ├─ Company
  ├─ CandidateProfile
  ├─ Resume
  ├─ JobPosting
  ├─ Application
  ├─ Tag
  ├─ Category
  ├─ MatchScore
  ├─ OtpCode
  ├─ AuditLog
  └─ CvTemplate

BaseService
  ├─ AuthenticationService
  ├─ OtpService
  ├─ ResumeService
  ├─ JobService
  ├─ ApplicationService
  ├─ MatchingService
  ├─ MailService
  └─ StorageService

BaseRepository
  ├─ UserRepository
  ├─ CompanyRepository
  ├─ ResumeRepository
  ├─ JobPostingRepository
  ├─ ApplicationRepository
  ├─ MatchScoreRepository
  ├─ TagRepository
  ├─ CategoryRepository
  ├─ OtpCodeRepository
  ├─ AuditLogRepository
  └─ CvTemplateRepository
```

### ✅ **2. Composition (Tổng Hợp)**

**Services use Repositories:**
```
AuthenticationService
  • UserRepository (find users)
  • OtpService (OTP logic)
  
ResumeService
  • ResumeRepository (CRUD)
  • TagRepository (tag management)
  • StorageService (file upload)

JobService
  • JobPostingRepository (CRUD)
  • MatchingService (scoring)
  • TagRepository (tag management)

ApplicationService
  • ApplicationRepository (CRUD)
  • MatchingService (calculate match)
  • MailService (send notifications)

MatchingService
  • MatchScoreRepository
  • ResumeRepository
  • JobPostingRepository
```

### ✅ **3. Encapsulation (Đóng Gói)**

**Access Modifiers:**
- `+` Public methods (API)
- `#` Protected methods (internal)
- `-` Private methods (implementation)

**Example - Resume class:**
```
- _raw_text: text (private)
- _validation_errors: List[str] (private)

# _parse_structure(): json (protected)
# _validate_skills(): bool (protected)

+ get_tags(): List[Tag] (public)
+ add_tag(tag): void (public)
+ generate_pdf(): str (public)
```

### ✅ **4. Abstraction (Trừu Tượng)**

**Abstract Base Classes:**
- `BaseService` - common service logic
- `BaseRepository` - common CRUD operations
- `BaseModel` - common attributes

**Interface-like Behavior:**
All repositories implement standard CRUD + domain queries

### ✅ **5. Polymorphism (Đa Hình)**

**Method Overriding:**
```
BaseRepository.create(data)
  └─ Generic: add & commit to DB

UserRepository.create(data)
  ├─ Override: hash password
  └─ Then call parent.create()
```

**Multiple Services Same Operation:**
```
AuthenticationService.login()
  - Method 1: email + password
  - Method 2: email + OTP

ResumeService.create_resume()
  - Method 1: from template
  - Method 2: from uploaded file
```

---

## 🎯 SOLID PRINCIPLES

### **S - Single Responsibility**
```
✓ UserRepository: only handle User CRUD
✓ AuthenticationService: only handle auth
✓ OtpService: only handle OTP logic
✓ MailService: only send emails
```

### **O - Open/Closed**
```
✓ BaseService: open for extension
✓ All new services: extends BaseService
✓ No need to modify base class
```

### **L - Liskov Substitution**
```
All repositories can substitute BaseRepository
all services can substitute BaseService
```

### **I - Interface Segregation**
```
✓ Only implement needed methods
✓ UserRepository doesn't implement location queries
✓ JobRepository implements location queries
```

### **D - Dependency Inversion**
```
✓ Services depend on Repository interfaces
✗ Not on concrete implementations
✓ Dependency injection used
```

---

## 🔄 DESIGN PATTERNS

### 1. **Repository Pattern**
- Abstraction layer for data access
- Easy to swap implementations
- Centralized query logic

### 2. **Service Layer Pattern**
- Encapsulates business logic
- Coordinates multiple repositories
- Used by controllers

### 3. **Factory Pattern**
```python
class ServiceFactory:
    @staticmethod
    def create_auth_service(db):
        user_repo = UserRepository(db)
        otp_service = OtpService(...)
        return AuthenticationService(user_repo, otp_service)
```

### 4. **Strategy Pattern**
```python
class MatchingService:
    # Different scoring strategies
    - score_skills_match()
    - score_experience_match()
    - score_location_match()
    # Combined with weights
```

### 5. **Observer Pattern**
```python
ApplicationService.submit_application():
    Notify: MailService (send email)
    Notify: AuditLogRepository (log action)
```

### 6. **Template Method Pattern**
```python
BaseService.execute(data):
    if not validate(data):
        raise error
    result = do_execute(data)  # Override in subclass
    return result
```

---

## 📑 CLASS RELATIONSHIPS

### **Inheritance Relationships**
```
BaseModel ◃── User (13 models inherit from BaseModel)
BaseService ◃── AuthenticationService (8 services inherit)
BaseRepository ◃── UserRepository (11 repos inherit)
```

### **Composition Relationships**
```
AuthenticationService ••→ UserRepository
                      ••→ OtpService
                         ••→ OtpCodeRepository
                         ••→ MailService

ResumeService ••→ ResumeRepository
              ••→ TagRepository
              ••→ StorageService

JobService ••→ JobPostingRepository
           ••→ MatchingService
           ••→ TagRepository

ApplicationService ••→ ApplicationRepository
                    ••→ MatchingService
                    ••→ MailService
```

### **Association Relationships**
```
One-to-One:
  User ─1:1─ Company (recruiter)
  User ─1:1─ CandidateProfile (candidate)

One-to-Many:
  User ─1:*─ Resume
  User ─1:*─ JobPosting
  User ─1:*─ Application
  Company ─1:*─ JobPosting
  Category ─1:*─ Tag

Many-to-Many:
  JobPosting ─*:*─ Tag (via job_tags)
  Resume ─*:*─ Tag (via resume_tags)

Aggregate Relations:
  JobPosting ─1:*─ Application
  JobPosting ─1:*─ MatchScore
  Resume ─1:*─ Application
  Resume ─1:*─ MatchScore
```

---

## 📊 METHODS BY CLASS TYPE

### **Entity Methods** (Domain Operations)
```
User:
  + is_recruiter(), is_candidate(), is_admin()
  + verify_password(), set_password()
  + check_is_authenticated()

Resume:
  + get_tags(), add_tag(), remove_tag()
  + generate_pdf(), generate_docx()
  + is_complete(), set_as_primary()
  + extract_text_from_file(), parse_structure()

JobPosting:
  + publish(), close()
  + get_applications(), get_match_candidates()
  + is_opened(), is_deadline_passed()
  + calculate_all_matches()

Application:
  + is_submitted(), can_withdraw(), withdraw()
  + update_status(), set_recruiter_note()
  + is_accepted(), is_rejected()
  + send_status_notification()

MatchScore:
  + get_score_percentage(), is_high_match()
  + get_skill_match_score(), get_experience_match_score()
  + get_location_match_score()
```

### **Service Methods** (Business Operations)
```
AuthenticationService:
  + login(), register(), logout()
  + verify_email()

ResumeService:
  + create_resume(), update_resume()
  + upload_resume_file(), generate_pdf(), generate_docx()
  + extract_skills(), add_tags(), set_primary()

JobService:
  + create_job(), publish_job(), close_job()
  + add_tags(), get_recommended_jobs()
  + search_jobs(), get_job_analytics()

ApplicationService:
  + submit_application(), update_app_status()
  + withdraw_application(), set_recruiter_note()
  + get_applications_for_job(), get_candidate_applications()
  + send_status_notification()

MatchingService:
  + calculate_match_score(), calculate_all_matches()
  + get_top_candidates(), get_recommended_jobs()

MailService:
  + send_otp_email(), send_app_status_email()
  + send_interview_invitation(), send_job_posted_notification()
```

### **Repository Methods** (Data Access)
```
BaseRepository:
  + find_by_id(), find_all()
  + create(), update(), delete()

Specialized Repositories Add:
  + find_by_role(), find_active_users() (UserRepository)
  + find_by_job(), find_by_status() (ApplicationRepository)
  + find_top_candidates(), find_recommended_jobs() (MatchScoreRepository)
  + find_by_location(), search() (JobPostingRepository)
```

---

## 🧪 TESTING BENEFITS

### **Easy Mocking**
```python
class MockUserRepository(BaseRepository):
    def find_by_id(self, user_id):
        return MagicMock(id=user_id)

@pytest.fixture
def auth_service():
    return AuthenticationService(MockUserRepository())
```

### **Unit Testing**
```python
def test_submit_application():
    app_repo = MockApplicationRepository()
    match_service = MockMatchingService()
    mail_service = MockMailService()
    
    service = ApplicationService(app_repo, match_service, mail_service)
    app = service.submit_application(1, 1, 1)
    
    assert app.status == "submitted"
```

### **Integration Testing**
```python
def test_job_posting_workflow(db):
    job_repo = JobPostingRepository(db)
    match_repo = MatchScoreRepository(db)
    job_service = JobService(job_repo, match_repo)
    
    job = job_service.create_job({...})
    job_service.publish_job(job.id)
    
    assert job.status == "published"
```

---

## 📁 PROJECT STRUCTURE

```
backend/
├── models/
│   ├── base.py              # BaseModel
│   ├── user.py              # User entity
│   ├── company.py           # Company entity
│   ├── resume.py            # Resume entity
│   ├── job_posting.py       # JobPosting entity
│   ├── application.py       # Application entity
│   ├── tag.py, category.py  # Tag hierarchy
│   ├── match_score.py       # MatchScore entity
│   ├── otp_code.py          # OtpCode entity
│   ├── audit_log.py         # AuditLog entity
│   └── cv_template.py       # CvTemplate entity

├── repositories/
│   ├── base.py              # BaseRepository
│   ├── users.py             # UserRepository
│   ├── resumes.py           # ResumeRepository
│   ├── jobs.py              # JobPostingRepository
│   ├── applications.py      # ApplicationRepository
│   ├── tags.py              # TagRepository, CategoryRepository
│   └── ...                  # 11 repositories total

├── services/
│   ├── base.py              # BaseService
│   ├── auth_service.py      # AuthenticationService
│   ├── otp_service.py       # OtpService
│   ├── resume_service.py    # ResumeService
│   ├── job_service.py       # JobService
│   ├── application_service.py # ApplicationService
│   ├── matching_service.py  # MatchingService
│   ├── mail_service.py      # MailService
│   └── storage_service.py   # StorageService

└── api/
    ├── auth.py              # Auth routes
    ├── resume_routes.py     # Resume routes
    ├── job_routes.py        # Job routes
    ├── application_routes.py # Application routes
    └── ...
```

---

## 🎓 KEY TAKEAWAYS

1. ✅ **Clear Separation**: Entities, Services, Repositories riêng biệt
2. ✅ **Inheritance**: Dùng base classes để code reuse
3. ✅ **Composition**: Services dùng repositories thay vì inheritance
4. ✅ **Encapsulation**: Private/protected/public methods rõ ràng
5. ✅ **Abstraction**: Abstract base classes định nghĩa contracts
6. ✅ **Polymorphism**: Method overriding cho specialization
7. ✅ **Dependency Injection**: Loose coupling, easy testing
8. ✅ **SOLID**: Tuân theo 5 nguyên tắc
9. ✅ **Design Patterns**: Repository, Service, Factory, Strategy
10. ✅ **Layered Architecture**: Clean code organization

---

## 📄 Files Generated

1. **JOB_PORTAL_CLASS_DIAGRAM.puml** - PlantUML class diagram (OOP-based)
2. **OOP_ARCHITECTURE_DESIGN.md** - Detailed architecture documentation
3. **BUSINESS_LOGIC_ANALYSIS.md** - Business logic & use cases (from before)
4. **OOP_CLASS_SUMMARY.md** - This file

**Bạn có thể render PlantUML diagram bằng:**
- Online: https://www.plantuml.com/plantuml/uml/
- VS Code Extension: PlantUML
- Command line: `plantuml JOB_PORTAL_CLASS_DIAGRAM.puml`
