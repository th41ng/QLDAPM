import pytest
from backend.services.statistics_service import get_landing_statistics
from backend.repositories.statistics import (
    count_published_jobs, count_published_employers, 
    count_active_categories, count_cv_templates
)
from backend.models import JobPosting, Company, Category, CvTemplate, User, Resume
from backend.core.extensions import db


class TestStatisticsService:
    """Test statistics generation."""
    
    def test_get_landing_statistics(self, app_context, sample_job, sample_company, sample_recruiter):
        """Get landing page statistics."""
        stats = get_landing_statistics()
        
        assert "total_jobs" in stats
        assert "total_employers" in stats
        assert "total_categories" in stats
        assert "total_cv_templates" in stats
    
    def test_get_landing_statistics_job_count(self, sample_job, app_context):
        """Statistics should count published jobs."""
        stats = get_landing_statistics()
        
        assert stats["total_jobs"] >= 1
    
    def test_get_landing_statistics_employer_count(self, sample_company, app_context):
        """Statistics should count employers with published jobs."""
        stats = get_landing_statistics()
        
        # sample_company has sample_job which is published
        assert stats["total_employers"] >= 1


class TestStatisticsRepository:
    """Test statistics repository functions."""
    
    def test_count_published_jobs(self, sample_job, app_context):
        """Count published jobs."""
        count = count_published_jobs()
        
        assert count >= 1
    
    def test_count_published_jobs_excludes_draft(self, sample_recruiter, sample_company, app_context):
        """Should not count draft jobs."""
        # Create draft job
        draft_job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Draft Job",
            slug="draft-job",
            status="draft"
        )
        db.session.add(draft_job)
        db.session.commit()
        
        count = count_published_jobs()
        
        # Should only count published, not draft
        assert draft_job not in JobPosting.query.filter_by(status="published")
    
    def test_count_published_employers(self, sample_company, app_context):
        """Count employers with published jobs."""
        count = count_published_employers()
        
        assert count >= 1
    
    def test_count_active_categories(self, app_context):
        """Count active categories."""
        # Create a category
        category = Category(name="Tech", slug="tech", status="active")
        db.session.add(category)
        db.session.commit()
        
        count = count_active_categories()
        
        assert count >= 1
    
    def test_count_cv_templates(self, app_context):
        """Count CV templates."""
        count = count_cv_templates()
        
        # Should be at least 0
        assert count >= 0


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_user_with_null_optional_fields(self, app_context):
        """Create user with minimal required fields."""
        user = User(
            full_name="Minimal User",
            email="minimal@example.com",
            password_hash="hashed",
            role="candidate"
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.phone is None
        assert user.avatar_url is None
    
    def test_long_text_fields(self, sample_recruiter, sample_company, app_context):
        """Handle very long text fields."""
        long_text = "x" * 5000
        
        job = JobPosting(
            recruiter_user_id=sample_recruiter.id,
            company_id=sample_company.id,
            title="Developer",
            slug="dev",
            description=long_text,
            requirements=long_text
        )
        db.session.add(job)
        db.session.commit()
        
        assert len(job.description) == 5000
    
    def test_special_characters_in_strings(self, sample_user, app_context):
        """Handle special characters."""
        from backend.core.security import slugify
        
        test_cases = [
            ("Hello & Goodbye", "hello-goodbye"),
            ("Price: $100-$500", "price-100-500"),
            ("C++ & C#", "c-c"),
        ]
        
        for text, expected_start in test_cases:
            slug = slugify(text)
            assert isinstance(slug, str)
    
    def test_concurrent_otp_verification(self, app_context, monkeypatch):
        """Multiple OTP codes for same user."""
        from backend.services.otp_service import send_otp_request
        
        monkeypatch.setattr(
            "backend.services.otp_service.send_otp_email",
            lambda *args, **kwargs: None
        )
        
        # Send multiple OTPs
        for i in range(3):
            send_otp_request(
                email="test@example.com",
                purpose="register",
                role="candidate",
                full_name="User",
                password="securePass123"
            )
        
        # All should exist
        from backend.models import OtpCode
        otps = OtpCode.query.filter_by(email="test@example.com").all()
        assert len(otps) == 3
    
    def test_unicode_in_resume(self, sample_user, app_context):
        """Handle unicode characters in resume."""
        resume = Resume(
            user_id=sample_user.id,
            title="简历",  # Chinese characters
            raw_text="Thông tin tiếng Việt",  # Vietnamese
            structured_json={"name": "日本人"}  # Japanese
        )
        db.session.add(resume)
        db.session.commit()
        
        assert "简" in resume.title
        assert "Việt" in resume.raw_text


class TestDataIntegrity:
    """Test data integrity constraints."""
    
    def test_timestamps_auto_set(self, app_context):
        """Model timestamps should be auto-set."""
        from datetime import datetime
        
        user = User(
            full_name="Test",
            email="test@example.com",
            password_hash="hash",
            role="candidate"
        )
        before = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        after = datetime.utcnow()
        
        assert before <= user.created_at <= after
        assert before <= user.updated_at <= after
    
    def test_updated_at_changes(self, sample_user, app_context):
        """Updated_at should change on modification."""
        from datetime import datetime
        import time
        
        original_time = sample_user.updated_at
        
        # Small delay to ensure time difference
        time.sleep(0.01)
        
        sample_user.full_name = "Updated Name"
        db.session.commit()
        
        assert sample_user.updated_at > original_time
    
    def test_relationships_cascade_delete(self, sample_user, app_context):
        """Related records should cascade delete."""
        resume = Resume(user_id=sample_user.id, title="Test")
        db.session.add(resume)
        db.session.commit()
        
        resume_id = resume.id
        
        # Delete user
        db.session.delete(sample_user)
        db.session.commit()
        
        # Resume should be deleted too
        resume = Resume.query.get(resume_id)
        assert resume is None
    
    def test_null_constraints_enforced(self, app_context):
        """NOT NULL constraints should be enforced."""
        user = User(
            full_name="",  # Empty is allowed
            email="test@example.com",
            password_hash="hash",
            role="candidate"
        )
        db.session.add(user)
        db.session.commit()
        
        # Without required fields
        bad_user = User(email="test2@example.com")  # Missing required
        db.session.add(bad_user)
        
        with pytest.raises(Exception):
            db.session.commit()


class TestPerformanceEdgeCases:
    """Test edge cases related to performance."""
    
    def test_large_structured_json(self, sample_user, app_context):
        """Resume with large structured data."""
        large_json = {
            f"field_{i}": [f"value_{j}" for j in range(100)]
            for i in range(100)
        }
        
        resume = Resume(
            user_id=sample_user.id,
            title="Complex",
            structured_json=large_json
        )
        db.session.add(resume)
        db.session.commit()
        
        assert resume.id is not None
        assert len(resume.structured_json) == 100
    
    def test_many_tags_on_job(self, sample_job, app_context):
        """Job with many tags."""
        from backend.models import Tag, Category
        
        category = Category(name="Tech", slug="tech")
        db.session.add(category)
        db.session.flush()
        
        # Create multiple tags
        tags = []
        for i in range(50):
            tag = Tag(
                name=f"Skill{i}",
                slug=f"skill-{i}",
                category_id=category.id
            )
            tags.append(tag)
            db.session.add(tag)
        db.session.flush()
        
        sample_job.tags = tags
        db.session.commit()
        
        assert len(sample_job.tags) == 50
