from sqlalchemy import func

from ..core.extensions import db
from ..models import Company, JobPosting


def get_company_by_user_id(user_id):
    return Company.query.filter_by(recruiter_user_id=user_id).first()


def list_companies():
    return Company.query.order_by(Company.created_at.desc()).all()


def list_featured_companies(limit=6):
    rows = (
        db.session.query(
            Company,
            func.count(JobPosting.id).label("openings"),
        )
        .join(JobPosting, JobPosting.company_id == Company.id)
        .filter(JobPosting.status == "published")
        .group_by(Company.id)
        .order_by(func.count(JobPosting.id).desc(), Company.created_at.desc())
        .limit(limit)
        .all()
    )
    return rows
