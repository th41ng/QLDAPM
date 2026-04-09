from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import json_error, json_ok, role_required
from ..core.extensions import db
from ..models import Application
from ..services.matching_service import store_match_score
from ..repositories import (
    application_exists,
    get_application_by_id,
    get_job_by_id,
    get_resume_by_id,
    get_user_by_id,
    list_candidate_applications,
    list_recruiter_applications,
)
from ..schemas import application_to_dict

api_applications_bp = Blueprint("api_applications", __name__)


@api_applications_bp.post("")
@jwt_required()
@role_required("candidate")
def create_application():
    user_id = get_jwt_identity()
    data = request.get_json(force=True)
    job_id = data.get("job_id")
    resume_id = data.get("resume_id")
    if not job_id or not resume_id:
        return json_error("job_id and resume_id are required.", 400)
    job = get_job_by_id(job_id)
    resume = get_resume_by_id(resume_id)
    if not job or not resume:
        return json_error("Job or resume not found.", 404)
    if resume.user_id != user_id:
        return json_error("Resume does not belong to you.", 403)
    exists = application_exists(user_id, job_id)
    if exists:
        return json_error("You already applied for this job.", 409)
    app = Application(
        candidate_user_id=user_id,
        job_id=job.id,
        resume_id=resume.id,
        cover_letter=data.get("cover_letter"),
        status="submitted",
    )
    db.session.add(app)
    db.session.add(store_match_score(resume, job, user_id))
    db.session.commit()
    return json_ok(application_to_dict(app), "Applied", 201)


@api_applications_bp.get("/mine")
@jwt_required()
@role_required("candidate")
def my_applications():
    user_id = get_jwt_identity()
    apps = list_candidate_applications(user_id)
    return json_ok([application_to_dict(app) for app in apps])


@api_applications_bp.get("/recruiter")
@jwt_required()
@role_required("recruiter", "admin")
def recruiter_applications():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    apps = list_recruiter_applications(None if user.role == "admin" else user_id)
    return json_ok([application_to_dict(app) for app in apps])


@api_applications_bp.patch("/<int:application_id>/status")
@jwt_required()
@role_required("recruiter", "admin")
def update_status(application_id):
    user_id = get_jwt_identity()
    app = get_application_by_id(application_id)
    if not app:
        return json_error("Application not found.", 404)
    user = get_user_by_id(user_id)
    if user.role != "admin" and app.job.recruiter_user_id != user_id:
        return json_error("Forbidden", 403)
    data = request.get_json(force=True)
    app.status = data.get("status", app.status)
    app.recruiter_note = data.get("recruiter_note", app.recruiter_note)
    db.session.commit()
    return json_ok(application_to_dict(app))


@api_applications_bp.get("/<int:application_id>/resume")
@jwt_required()
@role_required("recruiter", "admin")
def get_application_resume(application_id):
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    app = get_application_by_id(application_id)
    if not app:
        return json_error("Application not found.", 404)
    if user.role != "admin" and app.job.recruiter_user_id != user_id:
        return json_error("Forbidden", 403)
    return json_ok({
        "application": application_to_dict(app),
        "resume": None if not app.resume else {
            "id": app.resume.id,
            "title": app.resume.title,
            "raw_text": app.resume.raw_text,
            "structured_json": app.resume.structured_json,
            "file_ext": app.resume.file_ext,
            "stored_path": app.resume.stored_path,
        },
    })
