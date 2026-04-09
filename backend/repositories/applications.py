from sqlalchemy.orm import selectinload

from ..models import Application, JobPosting


def application_exists(candidate_user_id, job_id):
    return Application.query.filter_by(candidate_user_id=candidate_user_id, job_id=job_id).first()


def list_candidate_applications(candidate_user_id):
    return (
        Application.query.options(
            selectinload(Application.job),
            selectinload(Application.resume),
            selectinload(Application.candidate),
        )
        .filter_by(candidate_user_id=candidate_user_id)
        .order_by(Application.applied_at.desc())
        .all()
    )


def list_recruiter_applications(recruiter_user_id=None):
    query = Application.query.options(
        selectinload(Application.job),
        selectinload(Application.resume),
        selectinload(Application.candidate),
    ).join(JobPosting)
    if recruiter_user_id is not None:
        query = query.filter(JobPosting.recruiter_user_id == recruiter_user_id)
    return query.order_by(Application.applied_at.desc()).all()


def get_application_by_id(application_id):
    return Application.query.join(JobPosting).filter(Application.id == application_id).first()


def list_job_applications(job_id):
    return Application.query.filter_by(job_id=job_id).all()
