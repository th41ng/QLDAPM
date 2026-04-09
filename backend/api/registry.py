from .application_routes import api_applications_bp
from .auth import api_auth_bp
from .company_routes import api_companies_bp
from .job_routes import api_jobs_bp
from .profile_routes import api_profiles_bp
from .resume_routes import api_resumes_bp
from .statistics_routes import api_statistics_bp
from .tag_routes import api_tags_bp

API_PREFIXES = {
    "auth": "/api/auth",
    "jobs": "/api/jobs",
    "resumes": "/api/resumes",
    "profiles": "/api/profiles",
    "applications": "/api/applications",
    "companies": "/api/companies",
    "tags": "/api/tags",
    "statistics": "/api/statistics",
}

API_BLUEPRINTS = (
    (api_auth_bp, API_PREFIXES["auth"]),
    (api_jobs_bp, API_PREFIXES["jobs"]),
    (api_resumes_bp, API_PREFIXES["resumes"]),
    (api_profiles_bp, API_PREFIXES["profiles"]),
    (api_applications_bp, API_PREFIXES["applications"]),
    (api_companies_bp, API_PREFIXES["companies"]),
    (api_tags_bp, API_PREFIXES["tags"]),
    (api_statistics_bp, API_PREFIXES["statistics"]),
)


def register_api_blueprints(app):
    for blueprint, prefix in API_BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=prefix)
