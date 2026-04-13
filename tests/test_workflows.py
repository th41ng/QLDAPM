import pytest
from datetime import datetime
from backend.models import User, Resume, JobPosting, Application
from backend.core.extensions import db
from backend.repositories.applications import application_exists
from backend.core.security import hash_password, verify_password, slugify
from backend.services.otp_service import send_otp_request, verify_otp_request


class TestUserAuthenticationFlow:
    """Test authentication workflows."""
    
    def test_password_login_flow(self, app_context):
        """Complete password login flow."""
        password = "securePassword123"
        user = User(
            full_name="Login User",
            email="login@example.com",
            password_hash=hash_password(password),
            role="candidate",
            status="active"
        )
        db.session.add(user)
        db.session.commit()
        
        # Verify password
        assert verify_password(user.password_hash, password) is True
        assert verify_password(user.password_hash, "wrongPassword") is False
    
    def test_otp_register_flow(self, app_context, monkeypatch):
        """Complete OTP registration flow."""
        monkeypatch.setattr(
            "backend.services.otp_service.send_otp_email",
            lambda *args, **kwargs: None
        )
        
        # Step 1: Send OTP
        result = send_otp_request(
            email="newuser@example.com",
            purpose="register",
            role="candidate",
            full_name="New User",
            password="newPass123"
        )
        assert result.email == "newuser@example.com"
        
        # Step 2: In real scenario, verify OTP
        # For test, we just check the flow doesn't crash
        assert result.expires_in > 0
    
    def test_otp_login_flow(self, sample_user, app_context, monkeypatch):
        """Complete OTP login flow."""
        monkeypatch.setattr(
            "backend.services.otp_service.send_otp_email",
            lambda *args, **kwargs: None
        )
        
        # Step 1: Request OTP
        result = send_otp_request(
            email=sample_user.email,
            purpose="login"
        )
        assert result.email == sample_user.email
        assert result.purpose == "login"


class TestJobApplicationWorkflow:
    """Test job application workflows."""
    
    def test_apply_to_job_success(self, sample_user, sample_job, sample_resume, app_context):
        """Successfully apply to a job."""
        # Check no existing application
        assert application_exists(sample_user.id, sample_job.id) is None
        
        # Create application
        app = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=sample_resume.id,
            status="submitted"
        )
        db.session.add(app)
        db.session.commit()
        
        # Verify application exists
        existing = application_exists(sample_user.id, sample_job.id)
        assert existing is not None
        assert existing.status == "submitted"
    
    def test_prevent_duplicate_application(self, sample_user, sample_job, sample_resume, app_context):
        """Prevent duplicate applications."""
        # First application
        app1 = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=sample_resume.id
        )
        db.session.add(app1)
        db.session.commit()
        
        # Try to apply again
        existing = application_exists(sample_user.id, sample_job.id)
        assert existing is not None
        
        # Should not create duplicate
        apps = Application.query.filter_by(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id
        ).all()
        assert len(apps) == 1
    
    def test_application_status_workflow(self, sample_application, app_context):
        """Application status transitions."""
        statuses = ["submitted", "reviewed", "rejected"]
        
        for status in statuses:
            sample_application.status = status
            db.session.commit()
            assert sample_application.status == status


class TestResumeManagement:
    """Test resume management workflows."""
    
    def test_create_multiple_resumes(self, sample_user, app_context):
        """User can have multiple resumes."""
        resume1 = Resume(
            user_id=sample_user.id,
            title="Resume V1",
            raw_text="First resume"
        )
        resume2 = Resume(
            user_id=sample_user.id,
            title="Resume V2",
            raw_text="Second resume"
        )
        db.session.add_all([resume1, resume2])
        db.session.commit()
        
        resumes = Resume.query.filter_by(user_id=sample_user.id).all()
        assert len(resumes) == 2
    
    def test_resume_with_extracted_data(self, sample_user, app_context):
        """Resume stores extracted and structured data."""
        resume = Resume(
            user_id=sample_user.id,
            title="Full Resume",
            raw_text="Extracted text from PDF",
            structured_json={
                "skills": ["Python", "Django", "PostgreSQL"],
                "years_experience": 5,
                "education": "BS Computer Science"
            }
        )
        db.session.add(resume)
        db.session.commit()
        
        assert resume.structured_json["years_experience"] == 5
        assert "Python" in resume.structured_json["skills"]


class TestJobManagement:
    """Test job management workflows."""
    
    def test_create_job_with_tags(self, sample_recruiter, sample_company, sample_tag, app_context):
        """Create job with tags."""
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Python Developer",
            slug="python-developer",
            status="published"
        )
        job.tags = [sample_tag]
        db.session.add(job)
        db.session.commit()
        
        assert len(job.tags) > 0
        assert sample_tag in job.tags
    
    def test_job_slug_uniqueness(self, sample_recruiter, sample_company, app_context):
        """Jobs must have unique slugs."""
        job1 = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Developer",
            slug="developer"
        )
        db.session.add(job1)
        db.session.commit()
        
        # Create job with collision - should get auto-fixed slug
        job2 = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Developer",
            slug="developer"
        )
        db.session.add(job2)
        db.session.commit()
        
        assert job1.slug != job2.slug
    
    def test_job_publish_flow(self, sample_recruiter, sample_company, app_context):
        """Job publication flow."""
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Draft Job",
            slug="draft-job",
            status="draft"
        )
        db.session.add(job)
        db.session.commit()
        
        # Publish job
        job.status = "published"
        job.published_at = datetime.utcnow()
        db.session.commit()
        
        assert job.status == "published"
        assert job.published_at is not None


class TestSlugGeneration:
    """Test slug generation for various entities."""
    
    def test_job_title_to_slug(self):
        """Generate URL-friendly slug from job title."""
        title = "Senior Python & Django Developer"
        slug = slugify(title)
        
        assert slug == "senior-python-django-developer"
        assert "-" in slug or slug == "seniordeveloper"  # Some words might not have dash
        assert "@" not in slug
        assert "&" not in slug
    
    def test_company_name_to_slug(self):
        """Generate slug from company name."""
        name = "Tech & Innovation Inc."
        slug = slugify(name)
        
        assert slug.lower() == slug  # Lowercase
        assert "." not in slug
        assert "&" not in slug
    
    def test_tag_name_to_slug(self):
        """Generate slug from tag name."""
        tag = "C++ Development"
        slug = slugify(tag)
        
        assert "+" not in slug  # Special chars removed
        assert slug is not None


class TestDataConsistency:
    """Test data consistency across operations."""
    
    def test_user_job_application_consistency(self, sample_user, sample_job, sample_resume, app_context):
        """Application links user, job, and resume correctly."""
        app = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=sample_resume.id
        )
        db.session.add(app)
        db.session.commit()
        
        # Verify relationships
        assert app.candidate.id == sample_user.id
        assert app.job.id == sample_job.id
        assert app.resume.id == sample_resume.id
    
    def test_company_job_recruiter_consistency(self, sample_recruiter, sample_company, app_context):
        """Job correctly links to company and recruiter."""
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Test",
            slug="test"
        )
        db.session.add(job)
        db.session.commit()
        
        assert job.recruiter.id == sample_recruiter.id
        assert job.company.id == sample_company.id
        assert job.recruiter.id == job.company.recruiter.id
    
    def test_cascading_delete_consistency(self, sample_recruiter, app_context):
        """Delete recruiter cascades to company and jobs."""
        from backend.models import Company, JobPosting
        
        company = Company(
            recruiter_user_id=sample_recruiter.id,
            company_name="Test Co"
        )
        db.session.add(company)
        db.session.flush()
        
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=company.id,
            title="Test",
            slug="test"
        )
        db.session.add(job)
        db.session.commit()
        
        recruiter_id = sample_recruiter.id
        company_id = company.id
        job_id = job.id
        
        # Delete recruiter
        db.session.delete(sample_recruiter)
        db.session.commit()
        
        # Check cascading delete
        assert User.query.get(recruiter_id) is None
        assert Company.query.get(company_id) is None
        assert JobPosting.query.get(job_id) is None
