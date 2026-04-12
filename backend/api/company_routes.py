from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import json_error, json_ok, role_required
from ..core.extensions import db
from ..services.storage_service import upload_image
from ..models import Company
from ..repositories import get_company_by_user_id, get_user_by_id, list_featured_companies
from ..schemas import company_to_dict

api_companies_bp = Blueprint("api_companies", __name__)


@api_companies_bp.get("/me")
@jwt_required()
@role_required("recruiter", "admin")
def get_company():
    user = get_user_by_id(int(get_jwt_identity()))
    company = get_company_by_user_id(user.id)
    return json_ok(company_to_dict(company))


@api_companies_bp.put("/me")
@api_companies_bp.patch("/me")
@jwt_required()
@role_required("recruiter", "admin")
def update_company():
    user = get_user_by_id(int(get_jwt_identity()))
    data = request.get_json(force=True) if request.is_json else request.form.to_dict(flat=True)
    company = get_company_by_user_id(user.id)
    if not company:
        company = Company(recruiter_user_id=user.id, company_name=data.get("company_name", "").strip() or user.full_name)
        db.session.add(company)
    for field in ["company_name", "tax_code", "website", "address", "description", "logo_url", "industry"]:
        if field in data:
            setattr(company, field, data[field])
    logo_file = request.files.get("logo_file")
    if logo_file and logo_file.filename:
        uploaded = upload_image(logo_file, folder="jobportal/logos", public_id=f"company-{user.id}")
        if uploaded:
            company.logo_url = uploaded.url
    db.session.commit()
    return json_ok(company_to_dict(company))


@api_companies_bp.get("")
@jwt_required()
@role_required("admin")
def list_companies():
    from ..repositories import list_companies as list_company_records

    companies = list_company_records()
    return json_ok([company_to_dict(company) for company in companies])


@api_companies_bp.get("/featured")
def featured_companies():
    rows = list_featured_companies()
    payload = []
    for company, openings in rows:
        item = company_to_dict(company, openings=openings)
        item["badge"] = "Top" if openings and openings >= 3 else ""
        payload.append(item)
    return json_ok(payload)
