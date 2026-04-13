import pytest
from backend.core.services.matching_service import (
    tokenize, tag_text, score_resume_for_job, recommend_jobs_for_resume, _experience_floor
)
from backend.models import Resume, JobPosting, Tag, Category


class TestTokenize:
    """Test text tokenization for matching."""
    
    def test_tokenize_basic(self):
        """Tokenize simple text."""
        tokens = tokenize("Python Django PostgreSQL")
        assert "python" in tokens
        assert "django" in tokens
        assert "postgresql" in tokens
    
    def test_tokenize_removes_stopwords(self):
        """Remove common stopwords."""
        tokens = tokenize("Python and Django and JavaScript")
        assert "python" in tokens
        assert "django" in tokens
        assert "and" not in tokens
    
    def test_tokenize_lowercase(self):
        """Convert to lowercase."""
        tokens = tokenize("PYTHON Django JAVA")
        assert "python" in tokens
        assert "django" in tokens
        assert "java" in tokens
        assert not any(t.isupper() for t in tokens)
    
    def test_tokenize_removes_short_words(self):
        """Remove single character words."""
        tokens = tokenize("a Python b Django c Java")
        assert "python" in tokens
        assert "django" in tokens
        assert "java" in tokens
        assert "a" not in tokens
        assert "b" not in tokens
        assert "c" not in tokens
    
    def test_tokenize_extracts_numbers_and_symbols(self):
        """Keep numbers and tech symbols like + and #."""
        tokens = tokenize("C++ C# Python3.9")
        assert "c++" in tokens
        assert "c#" in tokens
        assert "python3" in tokens
    
    def test_tokenize_empty_string(self):
        """Handle empty string."""
        tokens = tokenize("")
        assert tokens == []
    
    def test_tokenize_none(self):
        """Handle None input."""
        tokens = tokenize(None)
        assert tokens == []
    
    def test_tokenize_special_pattern(self):
        """Handle special patterns."""
        tokens = tokenize("contact@example.com +1-234-567-8900")
        assert "contact" in tokens
        assert "example" in tokens


class TestTagText:
    """Test tag text generation."""
    
    def test_tag_text_with_description(self, sample_tag, app_context):
        """Generate text from tag with description."""
        text = tag_text(sample_tag)
        assert "python" in text.lower()
        assert "programming" in text.lower()
    
    def test_tag_text_without_category(self, app_context):
        """Generate text from tag without category."""
        tag = Tag(
            name="JavaScript",
            slug="javascript",
            description="Web scripting"
        )
        db_session = __import__('backend.core.extensions', fromlist=['db']).db.session
        db_session.add(tag)
        db_session.flush()
        
        text = tag_text(tag)
        assert "javascript" in text.lower()
        assert "web scripting" in text.lower()


class TestExperienceFloor:
    """Test experience level requirements."""
    
    def test_experience_floor_senior(self):
        """Senior level requires 5+ years."""
        assert _experience_floor("senior") == 5
        assert _experience_floor("Senior Developer") == 5
    
    def test_experience_floor_middle(self):
        """Middle level requires 3+ years."""
        assert _experience_floor("middle") == 3
        assert _experience_floor("mid-level") == 3
        assert _experience_floor("Mid-level") == 3
    
    def test_experience_floor_junior(self):
        """Junior level requires 0+ years."""
        assert _experience_floor("junior") == 0
        assert _experience_floor("fresher") == 0
        assert _experience_floor("Junior Developer") == 0
    
    def test_experience_floor_default(self):
        """Unknown level defaults to 1 year."""
        assert _experience_floor("expert") == 1
        assert _experience_floor("unknown") == 1
    
    def test_experience_floor_empty(self):
        """Empty string defaults to 1 year."""
        assert _experience_floor("") == 1
        assert _experience_floor(None) == 1


class TestScoreResumeForJob:
    """Test resume-job matching score calculation."""
    
    def test_score_resume_exact_keyword_match(self, app_context):
        """Resume with matching keywords should score higher."""
        resume = Resume(
            title="Python Developer",
            raw_text="Senior Python developer with Django and PostgreSQL experience",
            structured_json={"years_experience": 5, "desired_location": "Ho Chi Minh City"}
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Django Developer",
            summary="Looking for Python expert",
            description="Python Django PostgreSQL",
            requirements="5 years Python experience",
            responsibilities="Write Python code",
            location="Ho Chi Minh City",
            experience_level="senior",
            employment_type="full-time"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert "score" in result
        assert "breakdown" in result
        assert result["score"] > 0
        assert result["breakdown"]["text"] > 0
    
    def test_score_resume_no_match(self, app_context):
        """Non-matching resume should score 0."""
        resume = Resume(
            title="Sales Manager",
            raw_text="Sales experience in retail",
            structured_json={"years_experience": 3}
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Python Developer",
            summary="Python specialist needed",
            description="Expert Python developer",
            requirements="Python Django",
            responsibilities="Code review and development",
            experience_level="senior"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["score"] == 0
    
    def test_score_resume_empty_content(self, app_context):
        """Empty resume or job should score 0."""
        resume = Resume(
            title="",
            raw_text="",
            structured_json={}
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="",
            summary="",
            description="",
            requirements="",
            responsibilities=""
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["score"] == 0
    
    def test_score_resume_tag_matching(self, app_context):
        """Tag matching should increase score."""
        category = Category(name="Languages", slug="languages")
        app_context.session.add(category)
        app_context.session.flush()
        
        tag = Tag(name="Python", slug="python", category_id=category.id)
        app_context.session.add(tag)
        app_context.session.flush()
        
        resume = Resume(
            title="Python Developer",
            raw_text="Developer with Python experience",
            structured_json={"years_experience": 3}
        )
        resume.tags = [tag]
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Python Role",
            summary="Need Python developer",
            description="Python development",
            requirements="Python required",
            responsibilities="Python coding",
            experience_level="junior"
        )
        job.tags = [tag]
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["breakdown"]["tags"] > 0
    
    def test_score_resume_location_match(self, app_context):
        """Matching location should increase location score."""
        resume = Resume(
            title="Developer",
            raw_text="Python developer",
            structured_json={
                "years_experience": 3,
                "desired_location": "Ho Chi Minh City"
            }
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Python Developer",
            summary="Developer",
            description="Python",
            requirements="Python",
            responsibilities="Develop",
            location="Ho Chi Minh City",
            experience_level="junior"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["breakdown"]["location"] == 10.0
    
    def test_score_resume_experience_match(self, app_context):
        """Matching experience level should give experience score."""
        resume = Resume(
            title="Developer",
            raw_text="5 years experience",
            structured_json={"years_experience": 5}
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Senior Developer",
            summary="Senior position",
            description="Need senior developer",
            requirements="5+ years",
            responsibilities="Lead",
            experience_level="senior"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["breakdown"]["experience"] == 10.0
    
    def test_score_resume_experience_insufficient(self, app_context):
        """Insufficient experience should not get experience score."""
        resume = Resume(
            title="Junior Developer",
            raw_text="1 year experience",
            structured_json={"years_experience": 1}
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Senior Python Developer",
            summary="Senior position",
            description="Senior developer",
            requirements="5+ years required",
            responsibilities="Lead team",
            experience_level="senior"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["breakdown"]["experience"] == 0.0
    
    def test_score_resume_max_100(self, app_context):
        """Score should not exceed 100."""
        resume = Resume(
            title="Perfect Candidate",
            raw_text="Python Django PostgreSQL senior developer 10 years experience",
            structured_json={
                "years_experience": 10,
                "desired_location": "Ho Chi Minh City"
            }
        )
        app_context.session.add(resume)
        
        job = JobPosting(
            title="Python Developer",
            summary="We are hiring",
            description="Python Django PostgreSQL",
            requirements="Python Django",
            responsibilities="Python development",
            location="Ho Chi Minh City",
            experience_level="senior"
        )
        app_context.session.add(job)
        app_context.session.flush()
        
        result = score_resume_for_job(resume, job)
        
        assert result["score"] <= 100


class TestRecommendJobsForResume:
    """Test job recommendation for a resume."""
    
    def test_recommend_jobs_basic(self, app_context, sample_resume, sample_job):
        """Recommend jobs should return ranked jobs."""
        recommendations = recommend_jobs_for_resume(sample_resume, limit=5)
        
        assert isinstance(recommendations, list)
        # Should be sorted by score descending
        if len(recommendations) > 1:
            assert recommendations[0][0] >= recommendations[1][0]
    
    def test_recommend_jobs_respects_limit(self, app_context, sample_resume):
        """Respect limit parameter."""
        recommendations = recommend_jobs_for_resume(sample_resume, limit=3)
        
        assert len(recommendations) <= 3
    
    def test_recommend_jobs_returns_tuples(self, app_context, sample_resume, sample_job):
        """Each recommendation should be (score, job, breakdown) tuple."""
        recommendations = recommend_jobs_for_resume(sample_resume, limit=5)
        
        if recommendations:
            score, job, breakdown = recommendations[0]
            assert isinstance(score, (int, float))
            assert hasattr(job, "id")
            assert "text" in breakdown
            assert "tags" in breakdown
