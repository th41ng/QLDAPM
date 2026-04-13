import pytest
from datetime import datetime, timedelta
from backend.models import (
    User, CandidateProfile, Company, JobPosting, Application, Resume, MatchScore
)
from backend.core.extensions import db


class TestUserModel:
    """Test User model creation and validation."""
    
    def test_create_user_success(self, app_context):
        """Create user with required fields."""
        user = User(
            full_name="Jane Doe",
            email="jane@example.com",
            password_hash="hashed_password",
            role="candidate",
            status="active"
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.email == "jane@example.com"
        assert user.status == "active"
    
    def test_user_defaults(self, app_context):
        """User should have proper defaults."""
        user = User(
            full_name="Test User",
            email="test@example.com",
            password_hash="hashed",
            role="recruiter"
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.email_verified is False
        assert user.status == "active"
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_user_email_unique(self, sample_user, app_context):
        """Email should be unique."""
        duplicate_user = User(
            full_name="Duplicate",
            email=sample_user.email,
            password_hash="hashed",
            role="candidate"
        )
        db.session.add(duplicate_user)
        
        with pytest.raises(Exception):  # IntegrityError
            db.session.commit()


class TestCandidateProfileModel:
    """Test candidate profile creation."""
    
    def test_create_candidate_profile(self, sample_user, app_context):
        """Create candidate profile."""
        profile = CandidateProfile(
            user_id=sample_user.id,
            headline="Senior Developer",
            years_experience=5
        )
        db.session.add(profile)
        db.session.commit()
        
        assert profile.id is not None
        assert profile.user_id == sample_user.id
        assert profile.years_experience == 5
    
    def test_candidate_profile_relationships(self, sample_candidate_profile, app_context):
        """Profile should link to user."""
        assert sample_candidate_profile.user is not None
        assert sample_candidate_profile.user.role == "candidate"


class TestCompanyModel:
    """Test company model."""
    
    def test_create_company(self, sample_recruiter, app_context):
        """Create company for recruiter."""
        company = Company(
            recruiter_user_id=sample_recruiter.id,
            company_name="Tech Solutions",
            tax_code="123456789"
        )
        db.session.add(company)
        db.session.commit()
        
        assert company.id is not None
        assert company.recruiter_user_id == sample_recruiter.id
    
    def test_company_recruiter_relationship(self, sample_company, sample_recruiter, app_context):
        """Company should link to recruiter."""
        assert sample_company.recruiter is not None
        assert sample_company.recruiter.id == sample_recruiter.id


class TestJobPostingModel:
    """Test job posting model."""
    
    def test_create_job_posting(self, sample_recruiter, sample_company, app_context):
        """Create job posting."""
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Developer",
            slug="developer",
            status="published"
        )
        db.session.add(job)
        db.session.commit()
        
        assert job.id is not None
        assert job.status == "published"
    
    def test_job_posting_featured_flag(self, sample_job, app_context):
        """Job can be marked as featured."""
        sample_job.is_featured = True
        db.session.commit()
        
        assert sample_job.is_featured is True
    
    def test_job_posting_salary_range(self, app_context):
        """Job can have salary range."""
        job = JobPosting(
            title="Developer",
            slug="dev",
            salary_min=50000,
            salary_max=80000,
            salary_currency="USD"
        )
        
        assert job.salary_min == 50000
        assert job.salary_max == 80000


class TestResumeModel:
    """Test resume model."""
    
    def test_create_resume(self, sample_user, app_context):
        """Create resume."""
        resume = Resume(
            user_id=sample_user.id,
            title="My Resume",
            raw_text="Experience and skills",
            status="active"
        )
        db.session.add(resume)
        db.session.commit()
        
        assert resume.id is not None
        assert resume.user_id == sample_user.id
    
    def test_resume_structured_json(self, sample_resume, app_context):
        """Resume can store structured data."""
        assert sample_resume.structured_json is not None
        assert "skills" in sample_resume.structured_json
        assert "Python" in sample_resume.structured_json["skills"]


class TestApplicationModel:
    """Test application model."""
    
    def test_create_application(self, sample_user, sample_job, sample_resume, app_context):
        """Create job application."""
        app = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=sample_resume.id,
            status="submitted"
        )
        db.session.add(app)
        db.session.commit()
        
        assert app.id is not None
        assert app.status == "submitted"
    
    def test_application_timestamps(self, sample_application, app_context):
        """Application should have timestamps."""
        assert sample_application.applied_at is not None
    
    def test_application_status_workflow(self, sample_application, app_context):
        """Application status can change."""
        sample_application.status = "reviewed"
        db.session.commit()
        
        assert sample_application.status == "reviewed"


class TestApplicationBusinessLogic:
    """Test application business constraints."""
    
    def test_duplicate_application_prevented(self, sample_user, sample_job, sample_resume, app_context):
        """User cannot apply to same job twice with same resume."""
        # First application
        app1 = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=sample_resume.id
        )
        db.session.add(app1)
        db.session.commit()
        
        # Query should find existing
        from backend.repositories.applications import application_exists
        exists = application_exists(sample_user.id, sample_job.id)
        
        assert exists is not None
        assert exists.id == app1.id
    
    def test_application_with_different_resume_allowed(self, sample_user, sample_job, app_context):
        """User can apply with different resume."""
        resume1 = Resume(user_id=sample_user.id, title="Resume 1")
        resume2 = Resume(user_id=sample_user.id, title="Resume 2")
        db.session.add_all([resume1, resume2])
        db.session.flush()
        
        app1 = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=resume1.id
        )
        app2 = Application(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id,
            resume_id=resume2.id
        )
        db.session.add_all([app1, app2])
        db.session.commit()
        
        # Both should exist
        apps = list(Application.query.filter_by(
            candidate_user_id=sample_user.id,
            job_id=sample_job.id
        ))
        assert len(apps) == 2


class TestMatchScoreModel:
    """Test match score tracking."""
    
    def test_create_match_score(self, sample_resume, sample_job, app_context):
        """Create match score record."""
        score = MatchScore(
            resume_id=sample_resume.id,
            job_id=sample_job.id,
            score=85.5,
            breakdown={
                "text": 45,
                "tags": 20,
                "location": 10,
                "experience": 10.5
            }
        )
        db.session.add(score)
        db.session.commit()
        
        assert score.id is not None
        assert score.score == 85.5
        assert score.breakdown["text"] == 45
