def category_to_dict(category):
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "is_active": category.is_active,
    }


def tag_to_dict(tag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug,
        "category_id": tag.category_id,
        "category": tag.category.slug if tag.category else None,
        "category_name": tag.category.name if tag.category else None,
        "description": tag.description,
        "is_active": tag.is_active,
    }


def company_to_dict(company, openings=None):
    if not company:
        return None
    data = {
        "id": company.id,
        "recruiter_user_id": company.recruiter_user_id,
        "company_name": company.company_name,
        "tax_code": company.tax_code,
        "website": company.website,
        "address": company.address,
        "description": company.description,
        "logo_url": company.logo_url,
        "industry": company.industry,
    }
    if openings is not None:
        data["openings"] = int(openings or 0)
    return data


def profile_to_dict(profile):
    if not profile:
        return None
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "dob": profile.dob.isoformat() if profile.dob else None,
        "gender": profile.gender,
        "address": profile.address,
        "headline": profile.headline,
        "summary": profile.summary,
        "current_title": profile.current_title,
        "years_experience": profile.years_experience,
        "expected_salary": profile.expected_salary,
        "desired_location": profile.desired_location,
        "education": profile.education,
        "experience": profile.experience,
    }


def resume_to_dict(resume):
    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "title": resume.title,
        "source_type": resume.source_type,
        "template_name": resume.template_name,
        "original_filename": resume.original_filename,
        "stored_path": resume.stored_path,
        "file_ext": resume.file_ext,
        "mime_type": resume.mime_type,
        "raw_text": resume.raw_text,
        "structured_json": resume.structured_json,
        "generated_pdf_path": resume.generated_pdf_path,
        "generated_docx_path": resume.generated_docx_path,
        "is_primary": resume.is_primary,
        "tags": [tag_to_dict(tag) for tag in resume.tags],
    }


def job_to_dict(job):
    return {
        "id": job.id,
        "recruiter_user_id": job.recruiter_user_id,
        "company": company_to_dict(job.company),
        "title": job.title,
        "slug": job.slug,
        "summary": job.summary,
        "description": job.description,
        "requirements": job.requirements,
        "responsibilities": job.responsibilities,
        "location": job.location,
        "workplace_type": job.workplace_type,
        "employment_type": job.employment_type,
        "experience_level": job.experience_level,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "salary_currency": job.salary_currency,
        "vacancy_count": job.vacancy_count,
        "deadline": job.deadline.isoformat() if job.deadline else None,
        "status": job.status,
        "is_featured": job.is_featured,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "tags": [tag_to_dict(tag) for tag in job.tags],
    }


def application_to_dict(application):
    return {
        "id": application.id,
        "candidate_user_id": application.candidate_user_id,
        "job_id": application.job_id,
        "resume_id": application.resume_id,
        "cover_letter": application.cover_letter,
        "status": application.status,
        "recruiter_note": application.recruiter_note,
        "applied_at": application.applied_at.isoformat() if application.applied_at else None,
        "updated_at": application.updated_at.isoformat() if application.updated_at else None,
        "candidate": {
            "id": application.candidate.id,
            "full_name": application.candidate.full_name,
            "email": application.candidate.email,
        } if application.candidate else None,
        "job": job_to_dict(application.job) if application.job else None,
        "resume": resume_to_dict(application.resume) if application.resume else None,
    }
