import json
from pathlib import Path

from flask import Blueprint, current_app, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import json_error, json_ok, role_required
from ..core.extensions import db
from ..models import CandidateProfile, Resume, Tag
from ..services.cv_service import (
    allowed_resume_file,
    extract_text_from_upload,
    generate_docx_from_resume,
    generate_pdf_from_resume,
    save_uploaded_file,
)
from ..repositories import get_profile_by_user_id, get_resume_by_id, get_user_by_id, list_resumes_by_user_id
from ..schemas import resume_to_dict

api_resumes_bp = Blueprint("api_resumes", __name__)


def _current_user():
    return get_user_by_id(get_jwt_identity())


@api_resumes_bp.get("")
@jwt_required()
@role_required("candidate")
def list_resumes():
    user = _current_user()
    resumes = list_resumes_by_user_id(user.id)
    return json_ok([resume_to_dict(resume) for resume in resumes])


@api_resumes_bp.post("/manual")
@jwt_required()
@role_required("candidate")
def create_manual_resume():
    user = _current_user()
    data = request.get_json(force=True)
    resume = Resume(
        user_id=user.id,
        title=data.get("title") or f"CV của {user.full_name}",
        source_type="manual",
        template_name=data.get("template_name"),
        raw_text=json.dumps(data, ensure_ascii=False),
        structured_json={
            "full_name": data.get("full_name"),
            "headline": data.get("headline"),
            "summary": data.get("summary"),
            "skills": data.get("skills"),
            "experience": data.get("experience"),
            "education": data.get("education"),
            "desired_location": data.get("desired_location"),
            "years_experience": data.get("years_experience", 0),
        },
        is_primary=bool(data.get("is_primary", False)),
    )
    if resume.is_primary:
        Resume.query.filter_by(user_id=user.id, is_primary=True).update({"is_primary": False})
    db.session.add(resume)
    db.session.flush()
    tag_ids = data.get("tag_ids", [])
    if tag_ids:
        resume.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    profile = get_profile_by_user_id(user.id)
    if not profile:
        profile = CandidateProfile(user_id=user.id)
        db.session.add(profile)
    profile.headline = data.get("headline") or profile.headline
    profile.summary = data.get("summary") or profile.summary
    profile.education = data.get("education") or profile.education
    profile.experience = data.get("experience") or profile.experience
    profile.desired_location = data.get("desired_location") or profile.desired_location
    profile.years_experience = data.get("years_experience", profile.years_experience or 0)
    db.session.commit()
    return json_ok(resume_to_dict(resume), "Resume created", 201)


@api_resumes_bp.post("/upload")
@jwt_required()
@role_required("candidate")
def upload_resume():
    user = _current_user()
    if "file" not in request.files:
        return json_error("Resume file is required.", 400)
    file = request.files["file"]
    if not file.filename:
        return json_error("Resume file is required.", 400)
    if not allowed_resume_file(file.filename):
        return json_error("Only PDF, DOC and DOCX are supported.", 400)
    filename, stored_path, mime_type = save_uploaded_file(file, current_app.config["UPLOAD_FOLDER"], f"resume-{user.id}")
    extracted_text = extract_text_from_upload(stored_path)
    resume = Resume(
        user_id=user.id,
        title=request.form.get("title") or f"Uploaded CV {filename}",
        source_type="upload",
        original_filename=file.filename,
        stored_path=stored_path,
        file_ext=Path(file.filename).suffix.lower(),
        mime_type=mime_type,
        raw_text=extracted_text,
        structured_json={"extracted": True},
        is_primary=bool(request.form.get("is_primary", "false").lower() == "true"),
    )
    if resume.is_primary:
        Resume.query.filter_by(user_id=user.id, is_primary=True).update({"is_primary": False})
    db.session.add(resume)
    db.session.flush()
    tag_ids = [int(tag_id) for tag_id in request.form.getlist("tag_ids") if str(tag_id).isdigit()]
    if tag_ids:
        resume.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.commit()
    return json_ok(resume_to_dict(resume), "Resume uploaded", 201)


@api_resumes_bp.get("/<int:resume_id>")
@jwt_required()
def get_resume(resume_id):
    user = _current_user()
    resume = get_resume_by_id(resume_id)
    if not resume:
        return json_error("Resume not found.", 404)
    if user.role != "admin" and resume.user_id != user.id:
        return json_error("Forbidden", 403)
    return json_ok(resume_to_dict(resume))


@api_resumes_bp.put("/<int:resume_id>")
@api_resumes_bp.patch("/<int:resume_id>")
@jwt_required()
@role_required("candidate")
def update_resume(resume_id):
    user = _current_user()
    resume = Resume.query.filter_by(id=resume_id, user_id=user.id).first()
    if not resume:
        return json_error("Resume not found.", 404)
    data = request.get_json(force=True)
    for field in ["title", "template_name"]:
        if field in data:
            setattr(resume, field, data[field])
    if "raw_text" in data:
        resume.raw_text = data["raw_text"]
    if "structured_json" in data:
        resume.structured_json = data["structured_json"]
    if "is_primary" in data and data["is_primary"]:
        Resume.query.filter_by(user_id=user.id, is_primary=True).update({"is_primary": False})
        resume.is_primary = True
    if "tag_ids" in data:
        resume.tags = Tag.query.filter(Tag.id.in_(data["tag_ids"])).all()
    profile = get_profile_by_user_id(user.id)
    if profile and data.get("structured_json"):
        structured = data["structured_json"]
        profile.headline = structured.get("headline") or profile.headline
        profile.summary = structured.get("summary") or profile.summary
        profile.education = structured.get("education") or profile.education
        profile.experience = structured.get("experience") or profile.experience
        profile.desired_location = structured.get("desired_location") or profile.desired_location
        profile.years_experience = structured.get("years_experience", profile.years_experience or 0)
    db.session.commit()
    return json_ok(resume_to_dict(resume), "Resume updated")


@api_resumes_bp.delete("/<int:resume_id>")
@jwt_required()
@role_required("candidate")
def delete_resume(resume_id):
    user = _current_user()
    resume = Resume.query.filter_by(id=resume_id, user_id=user.id).first()
    if not resume:
        return json_error("Resume not found.", 404)
    db.session.delete(resume)
    db.session.commit()
    return json_ok(message="Resume deleted")


@api_resumes_bp.get("/<int:resume_id>/export")
@jwt_required()
@role_required("candidate", "recruiter", "admin")
def export_resume(resume_id):
    user = _current_user()
    resume = Resume.query.filter_by(id=resume_id).first()
    if not resume:
        return json_error("Resume not found.", 404)
    if user.role != "admin" and resume.user_id != user.id:
        return json_error("Forbidden", 403)
    fmt = request.args.get("format", "pdf").lower()
    data = {
        "full_name": resume.user.full_name,
        "headline": (resume.structured_json or {}).get("headline", ""),
        "summary": (resume.structured_json or {}).get("summary", ""),
        "skills": (resume.structured_json or {}).get("skills", ""),
        "experience": (resume.structured_json or {}).get("experience", ""),
        "education": (resume.structured_json or {}).get("education", ""),
    }
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    if fmt == "docx":
        path = upload_dir / f"resume-{resume.id}.docx"
        generate_docx_from_resume(data, str(path))
        return send_file(path, as_attachment=True, download_name=path.name)
    path = upload_dir / f"resume-{resume.id}.pdf"
    generate_pdf_from_resume(data, str(path))
    return send_file(path, as_attachment=True, download_name=path.name)


@api_resumes_bp.get("/recommendations")
@jwt_required()
@role_required("candidate")
def recommendations():
    user = _current_user()
    resumes = Resume.query.filter_by(user_id=user.id).all()
    from ..core.services.matching_service import recommend_jobs_for_resume
    recommendations_data = []
    for resume in resumes:
        for score, job, breakdown in recommend_jobs_for_resume(resume):
            recommendations_data.append({
                "resume_id": resume.id,
                "job_id": job.id,
                "score": score,
                "breakdown": breakdown,
            })
    recommendations_data.sort(key=lambda item: item["score"], reverse=True)
    return json_ok(recommendations_data)
