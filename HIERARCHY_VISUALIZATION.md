# OOP Class Hierarchy Visualization

## 🌳 CLASS INHERITANCE TREE

### 📦 HIERARCHY 1: Entity Models

```
BaseModel (Abstract)
│
├─ User
│   ├─ user_id
│   ├─ email
│   ├─ password_hash
│   ├─ role (admin, recruiter, candidate)
│   ├─ auth_method_preference
│   └─ Methods:
│       ├─ is_active()
│       ├─ is_recruiter()
│       ├─ is_candidate()
│       ├─ is_admin()
│       ├─ verify_password()
│       └─ set_password()
│
├─ Company
│   ├─ company_name
│   ├─ tax_code
│   ├─ website
│   ├─ address
│   ├─ logo_url
│   ├─ industry
│   └─ Methods:
│       ├─ get_recruiter_id()
│       ├─ get_job_count()
│       ├─ add_job()
│       └─ get_active_jobs()
│
├─ CandidateProfile
│   ├─ user_id
│   ├─ dob
│   ├─ headline
│   ├─ current_title
│   ├─ years_experience
│   ├─ expected_salary
│   └─ Methods:
│       ├─ get_user_id()
│       ├─ get_experience_level()
│       ├─ is_complete()
│       └─ calculate_match_score()
│
├─ Category
│   ├─ name
│   ├─ slug
│   ├─ description
│   ├─ is_active
│   └─ Methods:
│       ├─ get_tags()
│       ├─ add_tag()
│       └─ get_active_tags()
│
├─ Tag
│   ├─ name
│   ├─ slug
│   ├─ category_id
│   ├─ description
│   └─ Methods:
│       ├─ get_category()
│       ├─ activate()
│       ├─ deactivate()
│       └─ get_related_jobs()
│
├─ CvTemplate
│   ├─ name
│   ├─ slug
│   ├─ description
│   ├─ file_format (pdf, docx, both)
│   └─ Methods:
│       ├─ generate_resume()
│       ├─ get_preview_url()
│       └─ supports_format()
│
├─ Resume
│   ├─ user_id
│   ├─ title
│   ├─ source_type (manual, upload)
│   ├─ raw_text
│   ├─ structured_json
│   ├─ is_primary
│   └─ Methods:
│       ├─ get_user_id()
│       ├─ get_tags()
│       ├─ add_tag()
│       ├─ generate_pdf()
│       ├─ generate_docx()
│       ├─ set_as_primary()
│       ├─ is_complete()
│       └─ extract_text_from_file()
│
├─ JobPosting
│   ├─ recruiter_user_id
│   ├─ company_id
│   ├─ title
│   ├─ description
│   ├─ location
│   ├─ workplace_type (onsite, hybrid, remote)
│   ├─ employment_type (full-time, part-time)
│   ├─ experience_level (junior, senior, lead)
│   ├─ salary_min, salary_max
│   ├─ status (draft, published, closed)
│   └─ Methods:
│       ├─ publish()
│       ├─ close()
│       ├─ get_tags()
│       ├─ get_applications()
│       ├─ is_opened()
│       ├─ is_deadline_passed()
│       └─ calculate_all_matches()
│
├─ Application
│   ├─ candidate_user_id
│   ├─ job_id
│   ├─ resume_id
│   ├─ cover_letter
│   ├─ status (submitted, reviewing, interview, accepted, rejected)
│   └─ Methods:
│       ├─ get_candidate()
│       ├─ get_job()
│       ├─ get_resume()
│       ├─ can_withdraw()
│       ├─ withdraw()
│       ├─ update_status()
│       ├─ is_accepted()
│       └─ send_status_notification()
│
├─ MatchScore
│   ├─ job_id
│   ├─ resume_id
│   ├─ candidate_user_id
│   ├─ score (0-100)
│   ├─ breakdown_json
│   └─ Methods:
│       ├─ get_job()
│       ├─ get_resume()
│       ├─ get_score_percentage()
│       ├─ get_breakdown()
│       ├─ is_high_match()
│       └─ get_skill_match_score()
│
├─ OtpCode
│   ├─ user_id
│   ├─ email
│   ├─ role
│   ├─ purpose (register, login, reset)
│   ├─ code_hash
│   ├─ expires_at
│   ├─ attempts
│   └─ Methods:
│       ├─ is_expired()
│       ├─ is_used()
│       ├─ verify_code()
│       ├─ can_resend()
│       ├─ increment_attempts()
│       ├─ mark_as_used()
│       └─ get_payload()
│
└─ AuditLog
    ├─ actor_user_id
    ├─ action (create, update, delete)
    ├─ entity_type
    ├─ entity_id
    ├─ before_json
    ├─ after_json
    └─ Methods:
        ├─ get_actor()
        ├─ get_changes()
        ├─ was_created()
        ├─ was_updated()
        └─ get_change_summary()
```

---

### 🔧 HIERARCHY 2: Service Classes

```
BaseService (Abstract)
│
├─ AuthenticationService
│   ├─ Dependencies:
│   │   ├─ UserRepository
│   │   └─ OtpService
│   └─ Methods:
│       ├─ login(email, password)
│       ├─ register(data)
│       ├─ logout(user)
│       └─ verify_email(otp, code)
│
├─ OtpService
│   ├─ Dependencies:
│   │   ├─ OtpCodeRepository
│   │   └─ MailService
│   └─ Methods:
│       ├─ send_otp(email, purpose)
│       ├─ verify_otp(email, code)
│       ├─ resend_otp(email)
│       └─ check_max_attempts()
│
├─ ResumeService
│   ├─ Dependencies:
│   │   ├─ ResumeRepository
│   │   ├─ CvService
│   │   ├─ TagRepository
│   │   └─ StorageService
│   └─ Methods:
│       ├─ create_resume(data)
│       ├─ update_resume(id, data)
│       ├─ upload_resume_file(file)
│       ├─ generate_pdf(resume)
│       ├─ generate_docx(resume)
│       ├─ extract_skills(resume)
│       ├─ add_tags(resume_id, tags)
│       ├─ set_primary(resume_id)
│       └─ delete_resume(resume_id)
│
├─ JobService
│   ├─ Dependencies:
│   │   ├─ JobPostingRepository
│   │   ├─ MatchingService
│   │   └─ TagRepository
│   └─ Methods:
│       ├─ create_job(data)
│       ├─ publish_job(job_id)
│       ├─ close_job(job_id)
│       ├─ add_tags(job_id, tags)
│       ├─ get_recommended_jobs(limit)
│       ├─ search_jobs(filters)
│       └─ get_job_analytics(job_id)
│
├─ ApplicationService
│   ├─ Dependencies:
│   │   ├─ ApplicationRepository
│   │   ├─ MatchingService
│   │   └─ MailService
│   └─ Methods:
│       ├─ submit_application(candidate_id, job_id, resume_id)
│       ├─ update_app_status(app_id, status)
│       ├─ withdraw_application(app_id)
│       ├─ set_recruiter_note(app_id, note)
│       ├─ get_applications_for_job(job_id)
│       ├─ get_candidate_applications(candidate_id)
│       └─ send_status_notification(app)
│
├─ MatchingService
│   ├─ Dependencies:
│   │   ├─ MatchScoreRepository
│   │   ├─ ResumeRepository
│   │   └─ JobPostingRepository
│   └─ Methods:
│       ├─ calculate_match_score(job_id, resume_id)
│       ├─ calculate_all_matches(job_id)
│       ├─ get_top_candidates(job_id, limit)
│       ├─ get_recommended_jobs(resume_id, limit)
│       ├─ score_skills_match(job_tags, resume_tags)
│       ├─ score_experience_match(job, profile)
│       └─ score_location_match(job, profile)
│
├─ MailService
│   └─ Methods:
│       ├─ send_otp_email(email, code)
│       ├─ send_app_status_email(app)
│       ├─ send_interview_invitation(app)
│       ├─ send_job_posted_notification(recruiter, job)
│       └─ send_email(to, subject, body)
│
└─ StorageService
    └─ Methods:
        ├─ upload_file(file, path)
        ├─ delete_file(path)
        ├─ get_file(path)
        ├─ generate_pdf(data)
        └─ generate_docx(data)
```

---

### 💾 HIERARCHY 3: Repository Classes

```
BaseRepository (Abstract)
│
├─ UserRepository
│   ├─ Inherited Methods:
│   │   ├─ find_by_id(id)
│   │   ├─ find_all()
│   │   ├─ create(data)
│   │   ├─ update(id, data)
│   │   └─ delete(id)
│   └─ Specialized Methods:
│       ├─ find_by_email(email)
│       ├─ find_by_role(role)
│       ├─ find_active_users()
│       ├─ update_last_login(user_id)
│       ├─ lock_user(user_id)
│       └─ unlock_user(user_id)
│
├─ CompanyRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_recruiter(recruiter_id)
│       ├─ search_by_industry(industry)
│       └─ get_company_stats(company_id)
│
├─ ResumeRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_user(user_id)
│       ├─ find_primary_resume(user_id)
│       ├─ find_by_source_type(user_id, type)
│       └─ get_resume_with_tags(resume_id)
│
├─ JobPostingRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_status(status)
│       ├─ find_active_jobs()
│       ├─ find_by_recruiter(recruiter_id)
│       ├─ find_by_location(location)
│       ├─ search(filters)
│       ├─ find_published_jobs()
│       └─ get_featured_jobs(limit)
│
├─ ApplicationRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_job(job_id)
│       ├─ find_by_candidate(candidate_id)
│       ├─ find_by_status(status)
│       ├─ find_application(candidate_id, job_id)
│       ├─ exists_application(candidate_id, job_id)
│       └─ get_application_stats()
│
├─ MatchScoreRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_job(job_id)
│       ├─ find_by_resume(resume_id)
│       ├─ find_match(job_id, resume_id)
│       ├─ find_top_candidates(job_id, limit)
│       ├─ find_recommended_jobs(resume_id, limit)
│       └─ get_average_score(job_id)
│
├─ TagRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_category(category_id)
│       ├─ find_active_tags()
│       ├─ find_by_name(name)
│       ├─ find_job_tags(job_id)
│       └─ find_resume_tags(resume_id)
│
├─ CategoryRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_active_categories()
│       ├─ find_by_slug(slug)
│       └─ get_category_with_tags(category_id)
│
├─ OtpCodeRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_email_purpose(email, purpose)
│       ├─ find_pending(email)
│       ├─ find_by_ip_address(ip)
│       └─ cleanup_expired()
│
├─ AuditLogRepository
│   ├─ Inherited Methods: CRUD
│   └─ Specialized Methods:
│       ├─ find_by_actor(actor_id)
│       ├─ find_by_entity(entity_type, entity_id)
│       ├─ find_by_action(action)
│       ├─ find_by_ip_address(ip)
│       └─ get_daily_activity()
│
└─ CvTemplateRepository
    ├─ Inherited Methods: CRUD
    └─ Specialized Methods:
        ├─ find_active_templates()
        ├─ find_by_format(format)
        └─ find_by_slug(slug)
```

---

## 🔄 DEPENDENCY INJECTION GRAPH

```
Router/Controller
    │
    ├─→ AuthenticationService
    │       └─→ UserRepository
    │       └─→ OtpService
    │           └─→ OtpCodeRepository
    │           └─→ MailService
    │
    ├─→ ResumeService
    │       └─→ ResumeRepository
    │       └─→ TagRepository
    │       └─→ StorageService
    │
    ├─→ JobService
    │       └─→ JobPostingRepository
    │       └─→ MatchingService
    │           └─→ MatchScoreRepository
    │           └─→ ResumeRepository
    │           └─→ JobPostingRepository
    │       └─→ TagRepository
    │
    ├─→ ApplicationService
    │       └─→ ApplicationRepository
    │       └─→ MatchingService
    │           └─→ (see above)
    │       └─→ MailService
    │
    └─→ Other Services...
```

---

## 📊 ENTITY RELATIONSHIP DIAGRAM (OOP View)

```
User (1 Entity Class)
│
├─ 1-to-0..1 ──→ Company
├─ 1-to-0..1 ──→ CandidateProfile
├─ 1-to-* ────→ Resume (contains many)
├─ 1-to-* ────→ JobPosting (posted by recruiter)
├─ 1-to-* ────→ Application (submitted by candidate)
├─ 1-to-* ────→ OtpCode (requested)
└─ 1-to-* ────→ AuditLog (actor in)

              ┌─ Category
              │    │
              │    └─ 1-to-* ────→ Tag
              │                    │
              └──────────┬─────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        │                │                │
    Resume        JobPosting           (Others)
    carries       requires
    many-*        many-*
        │                │
        └────────────────┴────→ Tag (Both M-to-M)

Resume ────1-to-*───→ Application
JobPosting ────1-to-*───→ Application

Resume ────1-to-*───→ MatchScore
JobPosting ────1-to-*───→ MatchScore
User ────1-to-*───→ MatchScore
```

---

## 🎯 RESPONSIBILITY ASSIGNMENT (OOP Principle)

### What Each Layer Does:

**Models (Entities)**
- Store data attributes
- Implement domain-specific behaviors
- Validate state changes
- Provide getter/setter methods

**Services (Business Logic)**
- Orchestrate use cases
- Coordinate multiple repositories
- Implement business rules
- Handle transactions

**Repositories (Data Access)**
- Abstract database operations
- Provide query methods
- Ensure data consistency
- Handle ORM layer

**Controllers/Routes**
- Handle HTTP requests
- Validate input
- Call appropriate service
- Return responses

---

## 💡 KEY DESIGN DECISIONS

### ✅ Why Inheritance?
- Common attributes (id, created_at, updated_at)
- Common methods (save, delete, to_dict)
- Reduces code duplication
- Single point of change

### ✅ Why Composition?
- Services use Repositories instead of inheriting
- More flexible than deep inheritance hierarchies
- Can swap implementations
- Better testability

### ✅ Why Dependency Injection?
- Loose coupling between components
- Easy to mock for testing
- Can swap implementations at runtime
- Clear dependencies stated in constructor

### ✅ Why Abstract Base Classes?
- Define contracts for subclasses
- Enforce consistent interface
- Document expected behavior
- Enable polymorphism

---

## 📈 SCALABILITY CONSIDERATIONS

### Adding New Services
```
1. Create NewService(BaseService)
2. Inject required repositories
3. Implement execute(), validate()
4. Add to ServiceFactory
5. Wire into routes
```

### Adding New Repositories
```
1. Create NewRepository(BaseRepository)
2. Implement specialized find_* methods
3. Inject into appropriate services
4. Update service dependencies
```

### Adding New Entities
```
1. Create NewEntity(BaseModel)
2. Create NewRepository(BaseRepository)
3. Create corresponding service if needed
4. Implement domain-specific methods
5. Define relationships with other entities
```

---

## 🧪 TESTING STRATEGY

### Unit Tests (Repository Level)
```python
def test_create_user():
    repo = UserRepository(mock_db)
    user = repo.create({"email": "test@test.com"})
    assert user.email == "test@test.com"
```

### Integration Tests (Service Level)
```python
def test_submit_application():
    app_service = ApplicationService(app_repo, match_repo, mail_repo)
    app = app_service.submit_application(1, 1, 1)
    assert app.status == "submitted"
```

### End-to-End Tests (Controller Level)
```python
def test_application_workflow():
    # Create resume
    # Search jobs
    # Submit application
    # Check notification sent
    # Update status
    # Verify audit log
```

---

## 🚀 FUTURE EXTENSIBILITY

**Without changing existing code, we can add:**

1. ✅ New Services (extend BaseService)
2. ✅ New Repositories (extend BaseRepository)
3. ✅ New Entities (extend BaseModel)
4. ✅ New Notification Channels (implement MailService)
5. ✅ New Matching Algorithms (implement MatchingService)
6. ✅ New Storage Backends (implement StorageService)
7. ✅ New Authentication Methods (extend AuthenticationService)

**This is the Open/Closed Principle in action!**
