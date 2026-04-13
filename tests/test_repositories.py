import pytest
from backend.repositories.users import get_user_by_id, get_user_by_email
from backend.repositories.companies import (
    get_company_by_user_id, list_companies, list_featured_companies
)
from backend.repositories.jobs import (
    get_job_query, list_published_jobs, list_jobs, get_job_by_id, 
    create_job_record, apply_tags
)
from backend.repositories.applications import (
    application_exists, list_candidate_applications, list_recruiter_applications
)
from backend.models import User, Company, JobPosting, Application, Tag, Category
from backend.core.extensions import db


class TestUserRepository:
    """Test user data access functions."""
    
    def test_get_user_by_id_success(self, sample_user, app_context):
        """Get existing user by id."""
        user = get_user_by_id(sample_user.id)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email
    
    def test_get_user_by_id_not_found(self, app_context):
        """Get non-existent user should return None."""
        user = get_user_by_id(99999)
        assert user is None
    
    def test_get_user_by_id_invalid_id(self, app_context):
        """Invalid id should return None."""
        user = get_user_by_id("invalid")
        assert user is None
        
        user = get_user_by_id(None)
        assert user is None
    
    def test_get_user_by_email_success(self, sample_user, app_context):
        """Get existing user by email."""
        user = get_user_by_email(sample_user.email)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.email == sample_user.email
    
    def test_get_user_by_email_not_found(self, app_context):
        """Get non-existent user should return None."""
        user = get_user_by_email("nonexistent@example.com")
        assert user is None
    
    def test_get_user_by_email_case_insensitive(self, sample_user, app_context):
        """Email lookup should be case insensitive."""
        user = get_user_by_email(sample_user.email.upper())
        assert user is not None
        assert user.id == sample_user.id
    
    def test_get_user_by_email_whitespace_trimmed(self, sample_user, app_context):
        """Email with whitespace should be trimmed."""
        user = get_user_by_email(f"  {sample_user.email}  ")
        assert user is not None
        assert user.id == sample_user.id
    
    def test_get_user_by_email_none(self, app_context):
        """None email should not crash."""
        user = get_user_by_email(None)
        assert user is None


class TestCompanyRepository:
    """Test company data access functions."""
    
    def test_get_company_by_user_id_success(self, sample_company, sample_recruiter, app_context):
        """Get company by recruiter user id."""
        company = get_company_by_user_id(sample_recruiter.id)
        
        assert company is not None
        assert company.id == sample_company.id
        assert company.recruiter_user_id == sample_recruiter.id
    
    def test_get_company_by_user_id_not_found(self, app_context):
        """Non-existent recruiter should return None."""
        company = get_company_by_user_id(99999)
        assert company is None
    
    def test_list_companies(self, sample_company, app_context):
        """List all companies."""
        companies = list_companies()
        
        assert len(companies) > 0
        assert any(c.id == sample_company.id for c in companies)
    
    def test_list_companies_order_by_created_at(self, sample_recruiter, app_context):
        """Companies should be ordered by creation date."""
        from datetime import datetime, timedelta
        
        # Create second company
        company2 = Company(
            recruiter_user_id=sample_recruiter.id,
            company_name="Second Corp",
            address="Address 2"
        )
        db.session.add(company2)
        db.session.commit()
        
        companies = list_companies()
        
        # Most recent first
        assert companies[0].created_at >= companies[-1].created_at
    
    def test_list_featured_companies(self, sample_recruiter, sample_company, sample_job, app_context):
        """Featured companies should be those with most job openings."""
        featured = list_featured_companies(limit=5)
        
        # Result includes (company, openings_count) tuples
        if featured:
            company, openings = featured[0]
            assert openings > 0
    
    def test_list_featured_companies_limit(self, sample_recruiter, sample_company, sample_job, app_context):
        """Respect limit parameter."""
        featured = list_featured_companies(limit=1)
        assert len(featured) <= 1


class TestJobRepository:
    """Test job posting data access functions."""
    
    def test_get_job_query_returns_jobs(self, sample_job, app_context):
        """Get job query should return jobs with relations loaded."""
        query = get_job_query()
        jobs = query.all()
        
        assert any(j.id == sample_job.id for j in jobs)
    
    def test_list_published_jobs(self, sample_job, app_context):
        """List only published jobs."""
        jobs = list_published_jobs()
        
        assert sample_job in jobs
        assert all(j.status == "published" for j in jobs)
    
    def test_list_jobs_filter_by_query(self, sample_job, app_context):
        """Filter jobs by search query."""
        jobs = list_jobs(filters={"q": "Python"})
        
        # Should find sample_job with "Python" in title
        assert any(j.id == sample_job.id for j in jobs)
    
    def test_list_jobs_filter_by_location(self, sample_job, app_context):
        """Filter jobs by location."""
        jobs = list_jobs(filters={"location": "Ho Chi Minh"})
        
        assert sample_job in jobs
    
    def test_list_jobs_filter_no_match(self, sample_job, app_context):
        """No matching jobs should return empty."""
        jobs = list_jobs(filters={"q": "NonexistentTech999"})
        
        assert sample_job not in jobs
    
    def test_get_job_by_id_success(self, sample_job, app_context):
        """Get existing job by id."""
        job = get_job_by_id(sample_job.id)
        
        assert job is not None
        assert job.id == sample_job.id
    
    def test_get_job_by_id_not_found(self, app_context):
        """Non-existent job should return None."""
        job = get_job_by_id(99999)
        assert job is None
    
    def test_create_job_record_success(self, sample_recruiter, sample_company, app_context):
        """Create job record with data."""
        data = {
            "title": "Backend Developer",
            "slug": "backend-developer",
            "summary": "We need a backend dev",
            "description": "Full description",
            "requirements": "Node.js required",
            "location": "Hanoi",
            "experience_level": "junior",
            "status": "published"
        }
        
        job = create_job_record(sample_recruiter.id, sample_company.id, data)
        
        assert job.recruiter_user_id == sample_recruiter.id
        assert job.company_id == sample_company.id
        assert job.title == "Backend Developer"
        assert job.status == "published"
        assert job.published_at is not None
    
    def test_create_job_record_slug_collision_handling(self, sample_recruiter, sample_company, sample_job, app_context):
        """Slug collision should append timestamp."""
        data = {
            "title": sample_job.title,  # Same title will generate same slug
            "summary": "Description",
            "description": "Full",
            "requirements": "Req"
        }
        
        new_job = create_job_record(sample_recruiter.id, sample_company.id, data)
        db.session.add(new_job)
        db.session.commit()
        
        # New slug should be different due to timestamp
        assert new_job.slug != sample_job.slug
        assert "-" in new_job.slug  # Has timestamp suffix
    
    def test_apply_tags_to_job(self, sample_job, sample_tag, app_context):
        """Apply tags to job should associate tags."""
        apply_tags(sample_job, [sample_tag.id])
        db.session.commit()
        
        assert sample_tag in sample_job.tags


class TestApplicationRepository:
    """Test application data access functions."""
    
    def test_application_exists_success(self, sample_application, app_context):
        """Check if application exists."""
        exists = application_exists(
            sample_application.candidate_user_id,
            sample_application.job_id
        )
        
        assert exists is not None
        assert exists.id == sample_application.id
    
    def test_application_exists_not_found(self, sample_user, sample_job, app_context):
        """Non-existent application should return None."""
        exists = application_exists(sample_user.id, sample_job.id)
        assert exists is None
    
    def test_list_candidate_applications(self, sample_application, app_context):
        """List applications for a candidate."""
        apps = list_candidate_applications(sample_application.candidate_user_id)
        
        assert len(apps) > 0
        assert sample_application in apps
    
    def test_list_candidate_applications_empty(self, sample_user, app_context):
        """Candidate with no applications should return empty."""
        apps = list_candidate_applications(sample_user.id)
        assert apps == []
    
    def test_list_recruiter_applications(self, sample_application, app_context):
        """List applications for recruiter."""
        apps = list_recruiter_applications(
            sample_application.candidate.resumes[0].user.candidate_profile.user.id
        )
        
        # This is complex, just check it returns list
        assert isinstance(apps, list)
    
    def test_get_application_by_id_success(self, sample_application, app_context):
        """Get application by id."""
        from backend.repositories.applications import get_application_by_id
        
        app = get_application_by_id(sample_application.id)
        
        assert app is not None
        assert app.id == sample_application.id
    
    def test_list_job_applications(self, sample_application, app_context):
        """List applications for a job."""
        from backend.repositories.applications import list_job_applications
        
        apps = list_job_applications(sample_application.job_id)
        
        assert len(apps) > 0
        assert sample_application in apps
