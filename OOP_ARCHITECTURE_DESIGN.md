# Hệ Thống Thông Tin Tuyển Dụng - Thiết Kế OOP

## 📐 KIẾN TRÚC TỔNG THỂ (Overall Architecture)

Hệ thống được thiết kế theo mô hình **3-Layer Architecture** với OOP principles:

```
┌─────────────────────────────────────────────┐
│      Presentation Layer (Frontend)           │
│  (React Components, Forms, Pages)            │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────┐
│      Application Layer (Controllers)         │
│  (Route handlers, Request validation)        │
└──────────────────┬──────────────────────────┘
                   │ Dependency Injection
┌──────────────────▼──────────────────────────┐
│      BUSINESS LOGIC LAYER (Services)        │
│  - AuthenticationService                    │
│  - OtpService                               │
│  - ResumeService                            │
│  - JobService                               │
│  - ApplicationService                       │
│  - MatchingService                          │
│  - MailService                              │
│  - StorageService                           │
└──────────────────┬──────────────────────────┘
                   │ Dependency Injection
┌──────────────────▼──────────────────────────┐
│      DATA ACCESS LAYER (Repositories)        │
│  - UserRepository                           │
│  - ResumeRepository                         │
│  - JobPostingRepository                     │
│  - ApplicationRepository                    │
│  - MatchScoreRepository                     │
│  - TagRepository, CategoryRepository        │
│  - OtpCodeRepository, AuditLogRepository    │
└──────────────────┬──────────────────────────┘
                   │ ORM Query
┌──────────────────▼──────────────────────────┐
│      DATA MODEL LAYER (Components)          │
│  - User, Company, CandidateProfile          │
│  - Resume, JobPosting, Application          │
│  - Tag, Category, MatchScore                │
│  - OtpCode, AuditLog, CvTemplate            │
└──────────────────┬──────────────────────────┘
                   │ SQL Query
┌──────────────────▼──────────────────────────┐
│      DATABASE LAYER (MySQL)                 │
│  - 13 tables with relationships              │
│  - Indexes and constraints                  │
│  - Foreign key relationships                │
└─────────────────────────────────────────────┘
```

---

## 🏛️ OOP DESIGN PATTERNS

### 1. **Inheritance (Kế Thừa)**

#### A. Model Hierarchy (BaseModel)
```python
class BaseModel:
    """Base class cho tất cả entities"""
    - id: int (Primary Key)
    - created_at: datetime
    - updated_at: datetime
    
    + save(): void
    + delete(): void
    + to_dict(): dict
    + get_id(): int
```

**Subclasses (13 entities):**
- User, Company, CandidateProfile
- Category, Tag, CvTemplate
- Resume, JobPosting, Application
- MatchScore, OtpCode, AuditLog

**Benefits:**
- Code reuse for common attributes
- Consistent interface for all models
- Single point of maintenance for base functionality

#### B. Service Hierarchy (BaseService)
```python
class BaseService(ABC):
    """Abstract base class cho tất cả services"""
    - db_session: Session
    
    + execute(): any (abstract)
    + validate(): bool (abstract)
    + handle_error(): void
```

**Subclasses (8 services):**
- AuthenticationService
- OtpService
- ResumeService
- JobService
- ApplicationService
- MatchingService
- MailService
- StorageService

**Benefits:**
- Unified error handling
- Common transaction management
- Consistent validation interface

#### C. Repository Hierarchy (BaseRepository)
```python
class BaseRepository(ABC):
    """Abstract base class cho tất cả repositories"""
    - model: class
    - db: Session
    
    + find_by_id(id): T
    + find_all(): List[T]
    + create(data): T
    + update(id, data): T
    + delete(id): bool
```

**Subclasses (11 repositories):**
- UserRepository
- CompanyRepository
- ResumeRepository
- JobPostingRepository
- ApplicationRepository
- MatchScoreRepository
- TagRepository
- CategoryRepository
- OtpCodeRepository
- AuditLogRepository
- CvTemplateRepository

**Benefits:**
- Standardized CRUD operations
- Easy to mock for testing
- Database agnostic implementation

---

### 2. **Composition (Tổng Hợp)**

Services sử dụng composition thay vì inheritance để coordinate:

```
AuthenticationService
├── UserRepository (tìm user)
└── OtpService
    ├── OtpCodeRepository (quản lý OTP)
    └── MailService (gửi email)

ResumeService
├── ResumeRepository
├── TagRepository
└── StorageService

JobService
├── JobPostingRepository
├── MatchingService
└── TagRepository

ApplicationService
├── ApplicationRepository
├── MatchingService
└── MailService

MatchingService
├── MatchScoreRepository
├── ResumeRepository
└── JobPostingRepository
```

**Lợi ích:**
- Linh hoạt trong kết hợp tính năng
- Tránh Deep Hierarchy Problems
- Dễ testing isolated components

---

### 3. **Abstraction (Trừu Tượng Hóa)**

#### A. Abstract Base Classes
```python
from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def execute(self) -> Any:
        """Subclass phải implement"""
        pass
    
    def handle_error(self) -> None:
        """Common implementation"""
        pass
```

#### B. Interface-like Behavior
```python
class Repository:
    # Tất cả repositories implement 5 basic methods này
    - find_by_id(id)
    - find_all()
    - create(data)
    - update(id, data)
    - delete(id)
    
    # Plus domain-specific query methods
    - find_by_[field]()
    - search()
```

**Benefits:**
- Consistent contracts across implementations
- Easy to swap implementations
- Clear responsibilities

---

### 4. **Encapsulation (Đóng Gói)**

#### A. Access Modifiers

```python
class Resume:
    # Private (-)
    - _raw_text: text
    - _validation_errors: List[str]
    
    # Protected/Internal (#)
    # - parse_structure(): json
    # - validate_name(): bool
    
    # Public (+)
    + get_tags(): List[Tag]
    + add_tag(tag): void
    + generate_pdf(): str
    + is_complete(): bool
```

#### B. Information Hiding

```python
# Bad: Exposing internals
resume.structured_json = {}

# Good: Using methods
resume.update_structured_data(data)
```

#### C. Property Encapsulation

```python
class MatchScore:
    # Private: stores raw score
    - _score: float
    
    # Public methods to access
    + get_score_percentage(): float
    + is_high_match(): bool
    + get_breakdown(): dict
```

---

### 5. **Dependency Injection (Tiêm Phụ Thuộc)**

#### A. Constructor Injection
```python
class ApplicationService:
    def __init__(
        self,
        app_repo: ApplicationRepository,
        match_service: MatchingService,
        mail_service: MailService,
    ):
        self.app_repo = app_repo
        self.match_service = match_service
        self.mail_service = mail_service
```

**Benefits:**
- Loose coupling
- Easy mocking for tests
- Single Responsibility Principle

#### B. Service Registration (Flask Container)
```python
# In app initialization
def create_app():
    app = Flask(__name__)
    
    # Register repositories
    user_repo = UserRepository(db)
    resume_repo = ResumeRepository(db)
    
    # Register services with dependencies
    auth_service = AuthenticationService(user_repo, otp_service)
    resume_service = ResumeService(resume_repo, storage_service)
    
    # Inject into routes
    register_routes(app, auth_service, resume_service)
```

---

### 6. **Polymorphism (Đa Hình)**

#### A. Method Overriding
```python
class BaseRepository:
    def create(self, data):
        """Generic implementation"""
        entity = self.model(**data)
        db.session.add(entity)
        db.session.commit()
        return entity

class UserRepository(BaseRepository):
    def create(self, data):
        """User-specific creation"""
        # Hash password before creating
        data['password_hash'] = hash_password(data['password'])
        return super().create(data)
```

#### B. Method Overloading (Python style)
```python
class ResumeService:
    def update_resume(self, resume_id, data):
        """Update from dict"""
        resume = self.resume_repo.find_by_id(resume_id)
        resume.update(data)
        return resume
    
    def update_resume_from_file(self, resume_id, file):
        """Update from uploaded file"""
        text = self.extract_text(file)
        structured = self.parse_structure(text)
        return self.update_resume(resume_id, {'structured_json': structured})
```

#### C. Interface Implementation
```python
class MailService:
    """Implements Mail Service interface"""
    + send_otp_email(): bool
    + send_app_status_email(): bool
    + send_interview_invitation(): bool

class EmailNotificationService(MailService):
    """Email implementation"""
    def send_otp_email(self, email, code):
        # Send via email provider
        pass

class SmsNotificationService(MailService):
    """SMS implementation"""
    def send_otp_email(self, email, code):
        # Extract phone, send via SMS
        pass
```

---

## 🎯 SOLID PRINCIPLES APPLICATION

### S - Single Responsibility Principle
```
✓ UserRepository: chỉ xử lý User CRUD
✓ AuthenticationService: chỉ xử lý auth logic
✓ OtpService: chỉ xử lý OTP
✓ MailService: chỉ xử lý gửi mail

✗ AuditLogService: không nên xử lý cả audit và email
```

### O - Open/Closed Principle
```
✓ BaseService mở để extend (thêm service mới)
✓ Đóng để modify (không đổi base class)
✓ Thêm service mới chỉ cần extends BaseService

# New service mà không cần sửa BaseService
class NotificationService(BaseService):
    def execute(self):
        pass
```

### L - Liskov Substitution Principle
```
✓ Mọi Repository subclass có thể thay thế BaseRepository
✓ find_by_id() work giống nhau trên mọi repositories

user_repo: BaseRepository = UserRepository()
resume_repo: BaseRepository = ResumeRepository()
# Cả 2 đều có find_by_id() hoạt động giống nhau
```

### I - Interface Segregation Principle
```
✓ Repositories chỉ implement cần thiết
# UserRepository không cần implement find_by_location()
# JobRepository implement find_by_location()

✓ Services focused trên tác vụ cụ thể
# ResumeService không handle OTP
# OtpService không handle Resume
```

### D - Dependency Inversion Principle
```
✓ Services depend on Repository interfaces
✓ Không depend trực tiếp trên implementation

# Good:
class JobService:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

# Bad:
class JobService:
    def __init__(self):
        self.job_repo = JobPostgresRepository()  # Tight coupling!
```

---

## 🔄 DESIGN PATTERNS USED

### 1. **Repository Pattern** (Data Access Abstraction)
- Abstraction layer giữa service và database
- Dễ swap database implementation
- Centralized query logic

### 2. **Service Layer Pattern** (Business Logic)
- Encapsulates core business logic
- Coordinates multiple repositories
- Used by controllers/routes

### 3. **Factory Pattern** (Object Creation)
```python
class ServiceFactory:
    @staticmethod
    def create_auth_service(db):
        user_repo = UserRepository(db)
        otp_repo = OtpCodeRepository(db)
        otp_service = OtpService(otp_repo)
        return AuthenticationService(user_repo, otp_service)
```

### 4. **Strategy Pattern** (Matching Algorithm)
```python
class MatchingService:
    def calculate_match_score(self, job, resume):
        # Composition of strategies
        skill_score = self._score_skills(job.tags, resume.tags)
        exp_score = self._score_experience(job, resume)
        loc_score = self._score_location(job, resume)
        
        # Combine using weights
        total = (skill_score * 0.4 + 
                 exp_score * 0.3 + 
                 loc_score * 0.2)
        return total
```

### 5. **Observer Pattern** (Event Notification)
```python
class ApplicationService:
    def submit_application(self, candidate_id, job_id, resume_id):
        app = self.app_repo.create(...)
        
        # Observer: Notify via Event/Listener
        self.mail_service.send_confirmation(app)
        self.audit_service.log_action(app)
        
        return app
```

### 6. **Template Method Pattern** (BaseService)
```python
class BaseService:
    def execute(self, data):
        # Template
        if not self.validate(data):
            raise ValidationError()
        
        try:
            result = self.do_execute(data)
            return result
        except Exception as e:
            self.handle_error(e)

class ResumeService(BaseService):
    def do_execute(self, data):
        # Specific implementation
        return self._create_resume(data)
```

---

## 🔗 CLASS RELATIONSHIPS

### Composition Relationships
```
AuthenticationService → UserRepository
                     → OtpService
                        → OtpCodeRepository
                        → MailService

ResumeService → ResumeRepository
             → TagRepository
             → StorageService

JobService → JobPostingRepository
          → MatchingService
          → TagRepository
```

### Association Relationships
```
User ─────1:0..1────── Company
User ─────1:0..1────── CandidateProfile
User ─────1:*────── Resume
User ─────1:*────── JobPosting
User ─────1:*────── Application
User ─────1:*────── OtpCode
User ─────1:*────── AuditLog

Company ─────1:*────── JobPosting
Category ─────1:*────── Tag
JobPosting ─────*:*────── Tag (via JobTag_Junction)
Resume ─────*:*────── Tag (via ResumeTag_Junction)

JobPosting ─────1:*────── Application
JobPosting ─────1:*────── MatchScore

Resume ─────1:*────── Application
Resume ─────1:*────── MatchScore
```

---

## 📦 MODULES & ORGANIZATION

```
backend/
├── models/                    # ORM Models (BaseModel hierarchy)
│   ├── base.py               # BaseModel, junction tables
│   ├── user.py               # User, relationships
│   ├── company.py            # Company
│   ├── candidate_profile.py  # CandidateProfile
│   ├── resume.py             # Resume
│   ├── job_posting.py        # JobPosting
│   ├── application.py        # Application
│   ├── tag.py                # Tag hierarchy
│   ├── category.py           # Category
│   ├── match_score.py        # MatchScore
│   ├── otp_code.py           # OtpCode
│   ├── audit_log.py          # AuditLog
│   └── cv_template.py        # CvTemplate

├── repositories/             # Data Access Layer (BaseRepository hierarchy)
│   ├── __init__.py
│   ├── base.py               # BaseRepository (ABC)
│   ├── users.py              # UserRepository
│   ├── companies.py          # CompanyRepository
│   ├── resumes.py            # ResumeRepository
│   ├── jobs.py               # JobPostingRepository
│   ├── applications.py       # ApplicationRepository
│   ├── tags.py               # TagRepository, CategoryRepository
│   ├── match_scores.py       # MatchScoreRepository
│   ├── otp_codes.py          # OtpCodeRepository
│   └── audit_logs.py         # AuditLogRepository

├── services/                 # Business Logic Layer (BaseService hierarchy)
│   ├── __init__.py
│   ├── base.py               # BaseService (ABC)
│   ├── auth_service.py       # AuthenticationService
│   ├── otp_service.py        # OtpService
│   ├── resume_service.py     # ResumeService
│   ├── job_service.py        # JobService
│   ├── application_service.py# ApplicationService
│   ├── matching_service.py   # MatchingService
│   ├── mail_service.py       # MailService
│   └── storage_service.py    # StorageService

├── api/                      # API Controllers/Routes
│   ├── __init__.py
│   ├── auth.py               # Auth endpoints
│   ├── resume_routes.py      # Resume endpoints
│   ├── job_routes.py         # Job endpoints
│   ├── application_routes.py # Application endpoints
│   └── ...

└── core/
    ├── extensions.py         # Flask extensions (db, etc)
    ├── config.py             # Configuration
    └── security.py           # Security utilities
```

---

## 💡 TESTING & MOCK OBJECTS

### Repository Mocking
```python
class MockUserRepository(BaseRepository):
    def __init__(self):
        self.users = {}
    
    def find_by_id(self, user_id):
        return self.users.get(user_id)
    
    def create(self, data):
        user = User(**data)
        self.users[user.id] = user
        return user

# Usage in test
@pytest.fixture
def auth_service():
    mock_repo = MockUserRepository()
    return AuthenticationService(mock_repo)
```

### Service Testing
```python
def test_submit_application():
    # Mock repositories
    app_repo = MockApplicationRepository()
    match_service = MockMatchingService()
    mail_service = MockMailService()
    
    # Create service with mocks
    service = ApplicationService(app_repo, match_service, mail_service)
    
    # Test
    app = service.submit_application(candidate_id=1, job_id=1, resume_id=1)
    assert app.status == "submitted"
```

---

## 🎓 KEY TAKEAWAYS

1. **Inheritance** used for common attributes/methods (BaseModel, BaseService, BaseRepository)
2. **Composition** used to combine behaviors (Services use Repositories)
3. **Encapsulation** with access modifiers and properties
4. **Abstraction** via base classes and interfaces
5. **Polymorphism** through method overriding and interfaces
6. **Dependency Injection** for loose coupling and testability
7. **SOLID Principles** applied throughout
8. **Design Patterns** (Repository, Service, Factory, Strategy)
9. **Three-Layer Architecture** for separation of concerns
10. **Clear Responsibility** at each layer
