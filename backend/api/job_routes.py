from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import json_error, json_ok, role_required
from ..core.extensions import db
from ..repositories import (
    apply_tags,
    create_job_record,
    get_job_by_id,
    get_user_by_id,
    list_job_applications,
    list_jobs as list_job_records,
    list_jobs_for_recruiter,
    list_screenable_resumes,
)
from ..services.matching_service import store_match_score
from ..schemas import application_to_dict, job_to_dict

api_jobs_bp = Blueprint("api_jobs", __name__)


@api_jobs_bp.get("")
def list_jobs():
    jobs = list_job_records(request.args)
    return json_ok([job_to_dict(job) for job in jobs])


@api_jobs_bp.get("/mine")
@jwt_required()
@role_required("recruiter", "admin")
def list_my_jobs():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    status = request.args.get("status") or None
    jobs = list_jobs_for_recruiter(None if user.role == "admin" else user_id, status=status)
    return json_ok([job_to_dict(job) for job in jobs])


@api_jobs_bp.get("/<int:job_id>")
def job_detail(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return json_error("Job not found.", 404)
    return json_ok(job_to_dict(job))


@api_jobs_bp.post("")
@jwt_required()
@role_required("recruiter")
def create_job():
    user_id = get_jwt_identity()
    data = request.get_json(force=True)
    company = get_user_by_id(user_id).company
    if not company:
        return json_error("Recruiter company profile is required.", 400)
    job = create_job_record(user_id, company.id, data)
    db.session.add(job)
    db.session.flush()
    apply_tags(job, data.get("tag_ids", []))
    db.session.commit()
    return json_ok(job_to_dict(job), "Job created", 201)


@api_jobs_bp.patch("/<int:job_id>")
@api_jobs_bp.put("/<int:job_id>")
@jwt_required()
@role_required("recruiter", "admin")
def update_job(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return json_error("Job not found.", 404)
    user_id = get_jwt_identity()
    if job.recruiter_user_id != user_id and get_user_by_id(user_id).role != "admin":
        return json_error("Forbidden", 403)
    data = request.get_json(force=True)
    for field in ["title", "summary", "description", "requirements", "responsibilities", "location", "workplace_type", "employment_type", "experience_level", "salary_currency", "status"]:
        if field in data:
            setattr(job, field, data[field])
    for field in ["salary_min", "salary_max", "vacancy_count"]:
        if field in data:
            setattr(job, field, data[field])
    if "deadline" in data and data["deadline"]:
        job.deadline = datetime.fromisoformat(data["deadline"]).date()
    if "tag_ids" in data:
        apply_tags(job, data["tag_ids"])
    if job.status == "published" and not job.published_at:
        job.published_at = datetime.utcnow()
    db.session.commit()
    return json_ok(job_to_dict(job), "Job updated")


@api_jobs_bp.delete("/<int:job_id>")
@jwt_required()
@role_required("recruiter", "admin")
def delete_job(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return json_error("Job not found.", 404)
    user_id = get_jwt_identity()
    if job.recruiter_user_id != user_id and get_user_by_id(user_id).role != "admin":
        return json_error("Forbidden", 403)
    db.session.delete(job)
    db.session.commit()
    return json_ok(message="Job deleted")


@api_jobs_bp.get("/<int:job_id>/applications")
@jwt_required()
@role_required("recruiter", "admin")
def job_applications(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return json_error("Job not found.", 404)
    user_id = get_jwt_identity()
    if job.recruiter_user_id != user_id and get_user_by_id(user_id).role != "admin":
        return json_error("Forbidden", 403)
    apps = list_job_applications(job.id)
    return json_ok([application_to_dict(app) for app in apps])


@api_jobs_bp.get("/<int:job_id>/screen")
@jwt_required()
@role_required("recruiter", "admin")
def screen_job(job_id):
    job = get_job_by_id(job_id)
    if not job:
        return json_error("Job not found.", 404)
    user_id = get_jwt_identity()
    if job.recruiter_user_id != user_id and get_user_by_id(user_id).role != "admin":
        return json_error("Forbidden", 403)
    resumes = list_screenable_resumes()
    scored = []
    for resume in resumes:
        record = store_match_score(resume, job, resume.user_id)
        db.session.add(record)
        scored.append({
            "resume": {
                "id": resume.id,
                "user_id": resume.user_id,
                "title": resume.title,
                "candidate_name": resume.user.full_name if resume.user else None,
            },
            "score": record.score,
            "breakdown": record.breakdown_json,
        })
    db.session.commit()
    scored.sort(key=lambda item: item["score"], reverse=True)
    return json_ok(scored)
