import json
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload, selectinload
from werkzeug.utils import secure_filename

from ..core.extensions import db
from ..core.security import hash_password, slugify, verify_password
from ..core.services.storage_service import upload_image
from ..models import Application, CandidateProfile, Category, Company, CvTemplate, JobPosting, Resume, Tag, User

admin_bp = Blueprint("admin", __name__, template_folder="../templates")


ROLE_OPTIONS = ["admin", "recruiter", "candidate"]
USER_STATUS_OPTIONS = ["active", "locked"]
JOB_STATUS_OPTIONS = ["draft", "published", "closed"]
APPLICATION_STATUS_OPTIONS = ["submitted", "reviewing", "interview", "accepted", "rejected"]
FILE_FORMAT_OPTIONS = ["both", "pdf", "docx"]
DASHBOARD_PERIOD_OPTIONS = [
    ("7d", "7 ngày"),
    ("30d", "30 ngày"),
    ("90d", "90 ngày"),
    ("month", "Tháng này"),
    ("year", "Năm nay"),
]
DASHBOARD_JOB_STATUS_OPTIONS = [
    ("draft", "Nháp"),
    ("published", "Đang đăng"),
    ("closed", "Đã đóng"),
]
DASHBOARD_APPLICATION_STATUS_OPTIONS = [
    ("submitted", "Đã gửi"),
    ("reviewing", "Đang xem xét"),
    ("interview", "Phỏng vấn"),
    ("accepted", "Đã chấp nhận"),
    ("rejected", "Từ chối"),
    ("withdrawn", "Đã rút"),
]
DASHBOARD_ROLE_LABELS = {
    "admin": "Quản trị",
    "recruiter": "Nhà tuyển dụng",
    "candidate": "Ứng viên",
}
KPI_ICON_SVGS = {
    "blue": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>',
    "green": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 20h12"></path><path d="M6 16h12"></path><path d="M8 20V8l4-4 4 4v12"></path></svg>',
    "amber": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v4l3 3"></path><circle cx="12" cy="12" r="9"></circle></svg>',
    "red": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8v8"></path><path d="M8 12h8"></path><circle cx="12" cy="12" r="9"></circle></svg>',
    "slate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5V4"></path><path d="M4 19l16-5"></path><path d="M8 8h6"></path><path d="M8 12h4"></path></svg>',
}


CHART_COLORS = {
    "blue": "#2458f2",
    "green": "#059669",
    "amber": "#d97706",
    "red": "#dc2626",
    "slate": "#64748b",
    "violet": "#7c3aed",
    "cyan": "#0891b2",
}

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for("admin.login"))
        return fn(*args, **kwargs)

    return wrapper


def _to_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_bool(value):
    return str(value).lower() in {"1", "true", "on", "yes"}


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _commit(message, category="success"):
    db.session.commit()
    flash(message, category)


def _load_user_or_none(user_id):
    return db.session.get(User, user_id) if user_id else None


def _load_company_or_none(company_id):
    return db.session.get(Company, company_id) if company_id else None


def _load_category_or_none(category_id):
    return db.session.get(Category, category_id) if category_id else None


def _load_tag_or_none(tag_id):
    return db.session.get(Tag, tag_id) if tag_id else None


def _load_job_or_none(job_id):
    return db.session.get(JobPosting, job_id) if job_id else None


def _load_application_or_none(application_id):
    return db.session.get(Application, application_id) if application_id else None


def _load_template_or_none(template_id):
    return db.session.get(CvTemplate, template_id) if template_id else None


def _load_resume_or_none(resume_id):
    return db.session.get(Resume, resume_id) if resume_id else None


def _company_choices():
    return Company.query.order_by(Company.company_name.asc()).all()


def _recruiter_choices():
    return User.query.filter_by(role="recruiter").order_by(User.full_name.asc()).all()


def _category_choices():
    return Category.query.order_by(Category.name.asc()).all()


def _tag_choices():
    return Tag.query.join(Tag.category).order_by(Category.name.asc(), Tag.name.asc()).all()


def _save_admin_avatar(file_storage, user_id):
    if not file_storage or not getattr(file_storage, "filename", ""):
        return None

    uploaded = upload_image(file_storage, folder="jobportal/admin-avatars", public_id=f"admin-{user_id}")
    if uploaded:
        return uploaded.url

    static_folder = Path(current_app.static_folder) / "uploads" / "admin-avatars"
    static_folder.mkdir(parents=True, exist_ok=True)
    safe_name = secure_filename(file_storage.filename) or "avatar.png"
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"admin-{user_id}-{stamp}-{safe_name}"
    target = static_folder / filename
    file_storage.save(target)
    return url_for("static", filename=f"uploads/admin-avatars/{filename}")


def _delete_resume_files(resume):
    for file_path in (resume.stored_path, resume.generated_pdf_path, resume.generated_docx_path):
        if not file_path:
            continue
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
        except Exception:
            pass


def _build_chart_rows(items):
    total = sum(item[2] for item in items) or 1
    rows = []
    for key, label, count in items:
        rows.append(
            {
                "key": key,
                "label": label,
                "count": count,
                "percent": round((count / total) * 100, 1),
                "color": CHART_COLORS.get(key, "#2458f2"),
            }
        )
    return rows


def _build_pie_chart(rows):
    total = sum(row["count"] for row in rows)
    if not total:
        return {"total": 0, "gradient": "#edf2ff 0deg 360deg", "segments": []}

    start = 0.0
    segments = []
    gradient_parts = []
    for index, row in enumerate(rows):
        count = row["count"]
        sweep = 360.0 * count / total if total else 0
        end = 360.0 if index == len(rows) - 1 else start + sweep
        gradient_parts.append(f'{row["color"]} {start:.2f}deg {end:.2f}deg')
        segments.append(
            {
                "key": row["key"],
                "label": row["label"],
                "count": count,
                "color": row["color"],
                "percent": row["percent"],
            }
        )
        start = end

    return {"total": total, "gradient": ", ".join(gradient_parts), "segments": segments}


def _dashboard_cutoff(period):
    now = datetime.utcnow()
    if period == "7d":
        return now - timedelta(days=7)
    if period == "30d":
        return now - timedelta(days=30)
    if period == "90d":
        return now - timedelta(days=90)
    if period == "month":
        return datetime(now.year, now.month, 1)
    if period == "year":
        return datetime(now.year, 1, 1)
    return None


def _dashboard_period_label(period):
    lookup = dict(DASHBOARD_PERIOD_OPTIONS)
    return lookup.get(period, "30 ngày")


def _dashboard_status_label(options, value):
    lookup = dict(options)
    return lookup.get(value, "Tất cả")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and current_user.role == "admin":
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email, role="admin").first()
        if user and user.status == "active" and verify_password(user.password_hash, password):
            login_user(user)
            return redirect(url_for("admin.dashboard"))
        flash("Sai tài khoản hoặc mật khẩu admin.", "error")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    period = request.args.get("period", "30d").strip() or "30d"
    job_status = request.args.get("job_status", "all").strip() or "all"
    application_status = request.args.get("application_status", "all").strip() or "all"

    cutoff = _dashboard_cutoff(period)
    period_label = _dashboard_period_label(period)
    job_status_label = _dashboard_status_label(DASHBOARD_JOB_STATUS_OPTIONS, job_status)
    application_status_label = _dashboard_status_label(DASHBOARD_APPLICATION_STATUS_OPTIONS, application_status)

    user_period_query = User.query
    recruiter_period_query = User.query.filter(User.role == "recruiter")
    job_period_query = JobPosting.query
    application_period_query = Application.query
    resume_period_query = Resume.query

    if cutoff:
        user_period_query = user_period_query.filter(User.created_at >= cutoff)
        recruiter_period_query = recruiter_period_query.filter(User.created_at >= cutoff)
        job_period_query = job_period_query.filter(JobPosting.created_at >= cutoff)
        application_period_query = application_period_query.filter(Application.applied_at >= cutoff)
        resume_period_query = resume_period_query.filter(Resume.created_at >= cutoff)

    if job_status != "all":
        job_period_query = job_period_query.filter(JobPosting.status == job_status)
    if application_status != "all":
        application_period_query = application_period_query.filter(Application.status == application_status)

    total_users = User.query.count()
    total_recruiters = User.query.filter_by(role="recruiter").count()
    total_jobs = JobPosting.query.count()
    total_applications = Application.query.count()
    total_resumes = Resume.query.count()
    total_templates = CvTemplate.query.filter(CvTemplate.is_active.is_(True)).count()

    kpis = [
        {
            "key": "users",
            "label": "Người dùng mới",
            "value": user_period_query.count(),
            "note": f"Trong {period_label.lower()}",
            "icon": KPI_ICON_SVGS["blue"],
        },
        {
            "key": "recruiters",
            "label": "Nhà tuyển dụng mới",
            "value": recruiter_period_query.count(),
            "note": f"Trong {period_label.lower()}",
            "icon": KPI_ICON_SVGS["green"],
        },
        {
            "key": "jobs",
            "label": "Job mới",
            "value": job_period_query.count(),
            "note": f"Trạng thái: {job_status_label.lower()}",
            "icon": KPI_ICON_SVGS["amber"],
        },
        {
            "key": "applications",
            "label": "Application mới",
            "value": application_period_query.count(),
            "note": f"Trạng thái: {application_status_label.lower()}",
            "icon": KPI_ICON_SVGS["red"],
        },
        {
            "key": "resumes",
            "label": "CV mới",
            "value": resume_period_query.count(),
            "note": f"Trong {period_label.lower()}",
            "icon": KPI_ICON_SVGS["slate"],
        },
        {
            "key": "templates",
            "label": "Template hoạt động",
            "value": total_templates,
            "note": "Thư viện CV đang bật",
            "icon": KPI_ICON_SVGS["blue"],
        },
    ]
    users_by_role_query = User.query
    if cutoff:
        users_by_role_query = users_by_role_query.filter(User.created_at >= cutoff)
    users_by_role = _build_chart_rows(
        [
            ("admin", DASHBOARD_ROLE_LABELS["admin"], users_by_role_query.filter(User.role == "admin").count()),
            ("recruiter", DASHBOARD_ROLE_LABELS["recruiter"], users_by_role_query.filter(User.role == "recruiter").count()),
            ("candidate", DASHBOARD_ROLE_LABELS["candidate"], users_by_role_query.filter(User.role == "candidate").count()),
        ]
    )

    jobs_by_status_query = JobPosting.query
    if cutoff:
        jobs_by_status_query = jobs_by_status_query.filter(JobPosting.created_at >= cutoff)
    if job_status != "all":
        jobs_by_status_query = jobs_by_status_query.filter(JobPosting.status == job_status)
    jobs_by_status = _build_chart_rows(
        [
            ("draft", "Nháp", jobs_by_status_query.filter(JobPosting.status == "draft").count()),
            ("published", "Đang đăng", jobs_by_status_query.filter(JobPosting.status == "published").count()),
            ("closed", "Đã đóng", jobs_by_status_query.filter(JobPosting.status == "closed").count()),
        ]
    )

    applications_by_status_query = Application.query
    if cutoff:
        applications_by_status_query = applications_by_status_query.filter(Application.applied_at >= cutoff)
    if application_status != "all":
        applications_by_status_query = applications_by_status_query.filter(Application.status == application_status)
    applications_by_status = _build_chart_rows(
        [
            ("submitted", "Đã gửi", applications_by_status_query.filter(Application.status == "submitted").count()),
            ("reviewing", "Đang xem xét", applications_by_status_query.filter(Application.status == "reviewing").count()),
            ("interview", "Phỏng vấn", applications_by_status_query.filter(Application.status == "interview").count()),
            ("accepted", "Đã chấp nhận", applications_by_status_query.filter(Application.status == "accepted").count()),
            ("rejected", "Từ chối", applications_by_status_query.filter(Application.status == "rejected").count()),
            ("withdrawn", "Đã rút", applications_by_status_query.filter(Application.status == "withdrawn").count()),
        ]
    )

    resume_source_query = Resume.query
    if cutoff:
        resume_source_query = resume_source_query.filter(Resume.created_at >= cutoff)
    resume_source_rows = _build_chart_rows(
        [
            ("template", "Tạo từ mẫu", resume_source_query.filter(Resume.template_name.isnot(None)).count()),
            ("manual", "Tạo thủ công", resume_source_query.filter(Resume.source_type == "manual", Resume.template_name.is_(None)).count()),
            ("upload", "Upload", resume_source_query.filter(Resume.source_type == "upload").count()),
        ]
    )

    user_role_pie = _build_pie_chart(users_by_role)
    job_status_pie = _build_pie_chart(jobs_by_status)
    resume_source_pie = _build_pie_chart(resume_source_rows)


    chart_tabs = [
        {
            "key": "users",
            "tab_label": "Tài khoản",
            "eyebrow": "Người dùng",
            "title": "Phân bổ tài khoản theo vai trò",
            "description": "Cơ cấu admin, recruiter và candidate trong kỳ đã chọn.",
            "total": total_users,
            "unit": "tài khoản",
            "pie": user_role_pie,
            "rows": users_by_role,
            "empty": "Không có dữ liệu tài khoản trong kỳ này.",
        },
        {
            "key": "jobs",
            "tab_label": "Việc làm",
            "eyebrow": "Tin tuyển dụng",
            "title": "Trạng thái tin tuyển dụng",
            "description": "Biểu đồ tròn giúp nhìn nhanh tỷ lệ job theo trạng thái hoạt động.",
            "total": total_jobs,
            "unit": "job",
            "pie": job_status_pie,
            "rows": jobs_by_status,
            "empty": "Không có dữ liệu job trong kỳ này.",
        },
        {
            "key": "applications",
            "tab_label": "Ứng tuyển",
            "eyebrow": "Hồ sơ",
            "title": "Trạng thái hồ sơ ứng tuyến",
            "description": "Theo dõi luồng xử lý hồ sơ từ submitted đến accepted / rejected.",
            "total": total_applications,
            "unit": "application",
            "pie": _build_pie_chart(applications_by_status),
            "rows": applications_by_status,
            "empty": "Không có dữ liệu application trong kỳ này.",
        },
        {
            "key": "cv",
            "tab_label": "CV",
            "eyebrow": "Hồ sơ CV",
            "title": "Cơ cấu CV trong hệ thống",
            "description": "So sánh CV tạo từ mẫu, tạo thủ công và upload để nhìn nhanh thói quen sử dụng.",
            "total": total_resumes,
            "unit": "CV",
            "pie": resume_source_pie,
            "rows": resume_source_rows,
            "empty": "Không có dữ liệu CV trong kỳ này.",
        },
    ]
    top_jobs_query = (
        db.session.query(
            JobPosting,
            Company.company_name.label("company_name"),
            User.full_name.label("recruiter_name"),
            func.count(func.distinct(Application.id)).label("application_count"),
            func.max(Application.applied_at).label("last_application_at"),
        )
        .join(Company, Company.id == JobPosting.company_id)
        .join(User, User.id == JobPosting.recruiter_user_id)
        .outerjoin(Application, Application.job_id == JobPosting.id)
    )
    if cutoff:
        top_jobs_query = top_jobs_query.filter(JobPosting.created_at >= cutoff)
    if job_status != "all":
        top_jobs_query = top_jobs_query.filter(JobPosting.status == job_status)
    if application_status != "all":
        top_jobs_query = top_jobs_query.filter(Application.status == application_status)
    top_job_rows = (
        top_jobs_query.group_by(JobPosting.id, Company.company_name, User.full_name)
        .order_by(func.count(func.distinct(Application.id)).desc(), JobPosting.updated_at.desc())
        .limit(6)
        .all()
    )
    top_job_max = max((row.application_count or 0) for row in top_job_rows) or 1
    top_jobs = [
        {
            "id": job.id,
            "title": job.title,
            "slug": job.slug,
            "company": company_name,
            "recruiter": recruiter_name,
            "location": job.location,
            "status": job.status,
            "status_label": _dashboard_status_label(DASHBOARD_JOB_STATUS_OPTIONS, job.status),
            "applications": int(application_count or 0),
            "last_application_at": last_application_at,
            "percent": round(((application_count or 0) / top_job_max) * 100, 1),
            "featured": bool(job.is_featured),
        }
        for job, company_name, recruiter_name, application_count, last_application_at in top_job_rows
    ]

    recruiter_query = (
        db.session.query(
            User.id,
            User.full_name,
            User.email,
            User.status,
            Company.company_name,
            func.count(func.distinct(JobPosting.id)).label("job_count"),
            func.count(func.distinct(Application.id)).label("application_count"),
        )
        .outerjoin(Company, Company.recruiter_user_id == User.id)
        .outerjoin(JobPosting, JobPosting.recruiter_user_id == User.id)
        .outerjoin(Application, Application.job_id == JobPosting.id)
        .filter(User.role == "recruiter")
    )
    if cutoff:
        recruiter_query = recruiter_query.filter(or_(User.created_at >= cutoff, JobPosting.created_at >= cutoff, Application.applied_at >= cutoff))
    if job_status != "all":
        recruiter_query = recruiter_query.filter(JobPosting.status == job_status)
    if application_status != "all":
        recruiter_query = recruiter_query.filter(Application.status == application_status)
    recruiter_rows = (
        recruiter_query.group_by(User.id, User.full_name, User.email, User.status, Company.company_name)
        .order_by(func.count(func.distinct(JobPosting.id)).desc(), func.count(func.distinct(Application.id)).desc(), User.full_name.asc())
        .limit(6)
        .all()
    )
    recruiter_max = max((int(job_count or 0) + int(application_count or 0)) for _, _, _, _, _, job_count, application_count in recruiter_rows) or 1
    top_recruiters = [
        {
            "id": user_id,
            "name": full_name,
            "email": email,
            "status": status,
            "company": company_name,
            "jobs": int(job_count or 0),
            "applications": int(application_count or 0),
            "score": int(job_count or 0) + int(application_count or 0),
            "percent": round(((int(job_count or 0) + int(application_count or 0)) / recruiter_max) * 100, 1),
        }
        for user_id, full_name, email, status, company_name, job_count, application_count in recruiter_rows
    ]

    recent_apps_query = (
        Application.query.options(
            joinedload(Application.candidate),
            joinedload(Application.resume),
            joinedload(Application.job).joinedload(JobPosting.company),
        )
        .join(Application.job)
    )
    if cutoff:
        recent_apps_query = recent_apps_query.filter(Application.applied_at >= cutoff)
    if job_status != "all":
        recent_apps_query = recent_apps_query.filter(JobPosting.status == job_status)
    if application_status != "all":
        recent_apps_query = recent_apps_query.filter(Application.status == application_status)
    recent_applications = recent_apps_query.order_by(Application.applied_at.desc()).limit(6).all()

    filter_summary = [
        f"{period_label}",
        f"Job: {job_status_label}",
        f"Application: {application_status_label}",
    ]

    return render_template(
        "admin/dashboard.html",
        active_templates=total_templates,
        filter_summary=filter_summary,
        job_status=job_status,
        application_status=application_status,
        job_status_label=job_status_label,
        application_status_label=application_status_label,
        period=period,
        period_label=period_label,
        kpis=kpis,
        top_jobs=top_jobs,
        top_recruiters=top_recruiters,
        recent_applications=recent_applications,
        charts={
            "users_by_role": users_by_role,
            "jobs_by_status": jobs_by_status,
            "applications_by_status": applications_by_status,
            "resumes_by_source": resume_source_rows,
        },
        pie_charts={
            "users_by_role": user_role_pie,
            "jobs_by_status": job_status_pie,
            "applications_by_status": _build_pie_chart(applications_by_status),
            "resumes_by_source": resume_source_pie,
        },
        chart_tabs=chart_tabs,
        totals={
            "users": total_users,
            "recruiters": total_recruiters,
            "jobs": total_jobs,
            "applications": total_applications,
            "resumes": total_resumes,
            "templates": total_templates,
        },
        period_options=DASHBOARD_PERIOD_OPTIONS,
        job_status_options=DASHBOARD_JOB_STATUS_OPTIONS,
        application_status_options=DASHBOARD_APPLICATION_STATUS_OPTIONS,
    )


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@admin_required
def users():
    edit_id = request.args.get("edit", type=int)
    edit_user = _load_user_or_none(edit_id)
    page = request.args.get("page", 1, type=int)
    per_page = 6

    if request.method == "POST":
        action = request.form.get("action", "save")
        user_id = _to_int(request.form.get("user_id"))
        user = _load_user_or_none(user_id)

        if action == "toggle" and user:
            if user.id == current_user.id:
                flash("KhÃ´ng thá»ƒ khÃ³a chÃ­nh tÃ i khoáº£n admin Ä‘ang Ä‘Äƒng nháº­p.", "error")
            else:
                user.status = "locked" if user.status == "active" else "active"
                _commit("Đã cập nhật trạng thái tài khoản.")
            return redirect(url_for("admin.users", page=page))

        if action == "delete" and user:
            if user.id == current_user.id:
                flash("KhÃ´ng thá»ƒ xÃ³a chÃ­nh tÃ i khoáº£n admin Ä‘ang Ä‘Äƒng nháº­p.", "error")
            elif user.role == "admin" and User.query.filter_by(role="admin").count() <= 1:
                flash("Pháº£i giá»¯ láº¡i Ã­t nháº¥t má»™t tÃ i khoáº£n admin.", "error")
            else:
                db.session.delete(user)
                _commit("Đã xóa tài khoản.")
            return redirect(url_for("admin.users", page=page))

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "candidate").strip() or "candidate"
        status = request.form.get("status", "active").strip() or "active"
        phone = request.form.get("phone", "").strip() or None
        auth_method_preference = request.form.get("auth_method_preference", "password").strip() or "password"
        email_verified = _to_bool(request.form.get("email_verified"))
        avatar_file = request.files.get("avatar_file")

        if not full_name or not email or role not in ROLE_OPTIONS:
            flash("Vui lÃ²ng nháº­p Ä‘áº§y Ä‘á»§ tÃªn, email vÃ  vai trÃ².", "error")
            return redirect(url_for("admin.users", edit=user_id, page=page) if user_id else url_for("admin.users", page=page))

        existing = User.query.filter(User.email == email, User.id != (user.id if user else 0)).first()
        if existing:
            flash("Email nÃ y Ä‘Ã£ tá»“n táº¡i.", "error")
            return redirect(url_for("admin.users", edit=user.id if user else None, page=page))

        if user:
            user.full_name = full_name
            user.email = email
            user.role = role
            user.status = status if status in USER_STATUS_OPTIONS else user.status
            user.phone = phone
            user.auth_method_preference = auth_method_preference
            user.email_verified = email_verified
            avatar_url = _save_admin_avatar(avatar_file, user.id)
            if avatar_url:
                user.avatar_url = avatar_url
            if password:
                user.password_hash = hash_password(password)
            _commit("Đã cập nhật tài khoản.")
        else:
            if not password:
                flash("Máº­t kháº©u lÃ  báº¯t buá»™c khi táº¡o tÃ i khoáº£n.", "error")
                return redirect(url_for("admin.users", page=page))
            new_user = User(
                full_name=full_name,
                email=email,
                password_hash=hash_password(password),
                role=role,
                status=status if status in USER_STATUS_OPTIONS else "active",
                phone=phone,
                auth_method_preference=auth_method_preference,
                email_verified=email_verified,
            )
            db.session.add(new_user)
            db.session.flush()
            avatar_url = _save_admin_avatar(avatar_file, new_user.id)
            if avatar_url:
                new_user.avatar_url = avatar_url
            _commit("ÄÃ£ táº¡o tÃ i khoáº£n má»›i.")
        return redirect(url_for("admin.users", page=page))

    pagination = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    rows = pagination.items
    role_counts = {
        "admin": User.query.filter_by(role="admin").count(),
        "recruiter": User.query.filter_by(role="recruiter").count(),
        "candidate": User.query.filter_by(role="candidate").count(),
        "active": User.query.filter_by(status="active").count(),
        "locked": User.query.filter_by(status="locked").count(),
    }
    return render_template(
        "admin/users.html",
        users=rows,
        edit_user=edit_user,
        role_options=ROLE_OPTIONS,
        status_options=USER_STATUS_OPTIONS,
        total_users=pagination.total,
        role_counts=role_counts,
        pagination=pagination,
    )


@admin_bp.route("/resumes", methods=["GET", "POST"])
@login_required
@admin_required
def resumes():
    page = request.args.get("page", 1, type=int)
    view_id = request.args.get("view", type=int)
    q = request.args.get("q", "").strip()
    source_type = request.args.get("source_type", "").strip()
    primary_filter = request.args.get("primary", "").strip()
    role_filter = request.args.get("role", "").strip()
    per_page = 6

    if request.method == "POST":
        action = request.form.get("action", "").strip()
        resume_id = _to_int(request.form.get("resume_id"))
        resume = _load_resume_or_none(resume_id)

        if not resume:
            flash("Không tìm thấy hồ sơ CV.", "error")
            return redirect(url_for("admin.resumes", page=page, view=view_id))

        if action == "delete":
            was_primary = bool(resume.is_primary)
            user_id = resume.user_id
            _delete_resume_files(resume)
            db.session.delete(resume)
            db.session.flush()
            if was_primary:
                fallback = (
                    Resume.query.filter(Resume.user_id == user_id, Resume.id != resume_id)
                    .order_by(Resume.created_at.desc())
                    .first()
                )
                if fallback:
                    Resume.query.filter_by(user_id=user_id, is_primary=True).update({"is_primary": False})
                    fallback.is_primary = True
            _commit("Đã xóa hồ sơ CV.")
            return redirect(url_for("admin.resumes", page=page))

        if action == "primary":
            Resume.query.filter_by(user_id=resume.user_id, is_primary=True).update({"is_primary": False})
            resume.is_primary = True
            _commit("Đã đặt CV chính.")
            return redirect(url_for("admin.resumes", page=page, view=resume.id))

        flash("Hành động không hợp lệ.", "error")
        return redirect(url_for("admin.resumes", page=page, view=view_id))

    query = (
        Resume.query.options(
            joinedload(Resume.user).joinedload(User.candidate_profile),
            selectinload(Resume.tags),
            selectinload(Resume.applications),
            selectinload(Resume.match_scores),
        )
        .join(User)
    )

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Resume.title.ilike(like),
                Resume.template_name.ilike(like),
                Resume.original_filename.ilike(like),
                User.full_name.ilike(like),
                User.email.ilike(like),
            )
        )

    if source_type in {"manual", "upload", "generated"}:
        query = query.filter(Resume.source_type == source_type)

    if primary_filter == "primary":
        query = query.filter(Resume.is_primary.is_(True))
    elif primary_filter == "secondary":
        query = query.filter(Resume.is_primary.is_(False))

    if role_filter in ROLE_OPTIONS:
        query = query.filter(User.role == role_filter)

    pagination = query.order_by(Resume.is_primary.desc(), Resume.updated_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )
    rows = pagination.items
    selected_resume = _load_resume_or_none(view_id) if view_id else None
    if selected_resume:
        selected_resume = (
            Resume.query.options(
                joinedload(Resume.user).joinedload(User.candidate_profile),
                selectinload(Resume.tags),
                selectinload(Resume.applications),
                selectinload(Resume.match_scores),
            )
            .filter_by(id=selected_resume.id)
            .first()
        )

    selected_json = ""
    if selected_resume:
        selected_json = json.dumps(selected_resume.structured_json or {}, ensure_ascii=False, indent=2)

    return render_template(
        "admin/resumes.html",
        resumes=rows,
        pagination=pagination,
        selected_resume=selected_resume,
        selected_json=selected_json,
        total_resumes=Resume.query.count(),
        primary_resumes=Resume.query.filter_by(is_primary=True).count(),
        manual_resumes=Resume.query.filter_by(source_type="manual").count(),
        upload_resumes=Resume.query.filter_by(source_type="upload").count(),
        candidate_resumes=db.session.query(func.count(func.distinct(Resume.user_id))).scalar() or 0,
        q=q,
        source_type=source_type,
        primary_filter=primary_filter,
        role_filter=role_filter,
        resume_source_options=["manual", "upload", "generated"],
        role_options=ROLE_OPTIONS,
    )


@admin_bp.route("/companies", methods=["GET", "POST"])
@login_required
@admin_required
def companies():
    edit_id = request.args.get("edit", type=int)
    edit_company = _load_company_or_none(edit_id)
    recruiters = _recruiter_choices()

    if request.method == "POST":
        action = request.form.get("action", "save")
        company_id = _to_int(request.form.get("company_id"))
        company = _load_company_or_none(company_id)

        if action == "delete" and company:
            db.session.delete(company)
            _commit("Đã xóa công ty.")
            return redirect(url_for("admin.companies"))

        recruiter_user_id = _to_int(request.form.get("recruiter_user_id"))
        company_name = request.form.get("company_name", "").strip()
        tax_code = request.form.get("tax_code", "").strip() or None
        website = request.form.get("website", "").strip() or None
        address = request.form.get("address", "").strip() or None
        description = request.form.get("description", "").strip() or None
        logo_url = request.form.get("logo_url", "").strip() or None
        industry = request.form.get("industry", "").strip() or None

        if not recruiter_user_id or not company_name:
            flash("Vui lòng chọn recruiter và nhập tên công ty.", "error")
            return redirect(url_for("admin.companies", edit=company_id) if company_id else url_for("admin.companies"))

        recruiter = _load_user_or_none(recruiter_user_id)
        if not recruiter or recruiter.role != "recruiter":
            flash("Recruiter khÃ´ng há»£p lá»‡.", "error")
            return redirect(url_for("admin.companies", edit=company_id) if company_id else url_for("admin.companies"))

        duplicate = Company.query.filter(Company.recruiter_user_id == recruiter_user_id, Company.id != (company.id if company else 0)).first()
        if duplicate:
            flash("Recruiter nÃ y Ä‘Ã£ cÃ³ cÃ´ng ty rá»“i.", "error")
            return redirect(url_for("admin.companies", edit=company.id if company else None))

        if company:
            company.recruiter_user_id = recruiter_user_id
            company.company_name = company_name
            company.tax_code = tax_code
            company.website = website
            company.address = address
            company.description = description
            company.logo_url = logo_url
            company.industry = industry
            _commit("Đã cập nhật công ty.")
        else:
            db.session.add(
                Company(
                    recruiter_user_id=recruiter_user_id,
                    company_name=company_name,
                    tax_code=tax_code,
                    website=website,
                    address=address,
                    description=description,
                    logo_url=logo_url,
                    industry=industry,
                )
            )
            _commit("ÄÃ£ táº¡o cÃ´ng ty má»›i.")
        return redirect(url_for("admin.companies"))

    rows = Company.query.order_by(Company.created_at.desc()).all()
    return render_template(
        "admin/companies.html",
        companies=rows,
        recruiters=recruiters,
        edit_company=edit_company,
        total_companies=len(rows),
    )


@admin_bp.route("/jobs", methods=["GET", "POST"])
@login_required
@admin_required
def jobs():
    edit_id = request.args.get("edit", type=int)
    edit_job = _load_job_or_none(edit_id)
    companies = _company_choices()
    tags = _tag_choices()
    filter_q = request.args.get("q", "").strip()
    filter_status = request.args.get("status", "").strip()
    filter_company_id = _to_int(request.args.get("company_id"))
    filter_tag_id = _to_int(request.args.get("tag_id"))
    filter_featured = request.args.get("featured", "").strip()

    if request.method == "POST":
        action = request.form.get("action", "save")
        job_id = _to_int(request.form.get("job_id"))
        job = _load_job_or_none(job_id)

        if action == "delete" and job:
            db.session.delete(job)
            _commit("Đã xóa job.")
            return redirect(url_for("admin.jobs"))

        company_id = _to_int(request.form.get("company_id"))
        company = _load_company_or_none(company_id)
        title = request.form.get("title", "").strip()
        slug_value = request.form.get("slug", "").strip()
        summary = request.form.get("summary", "").strip() or None
        description = request.form.get("description", "").strip()
        requirements = request.form.get("requirements", "").strip()
        responsibilities = request.form.get("responsibilities", "").strip() or None
        location = request.form.get("location", "").strip()
        workplace_type = request.form.get("workplace_type", "onsite").strip()
        employment_type = request.form.get("employment_type", "full-time").strip()
        experience_level = request.form.get("experience_level", "junior").strip()
        salary_currency = request.form.get("salary_currency", "VND").strip()
        salary_min = _to_int(request.form.get("salary_min"))
        salary_max = _to_int(request.form.get("salary_max"))
        vacancy_count = _to_int(request.form.get("vacancy_count"), 1) or 1
        deadline = _parse_date(request.form.get("deadline", "").strip())
        status = request.form.get("status", "draft").strip()
        is_featured = _to_bool(request.form.get("is_featured"))
        tag_ids = [_to_int(value) for value in request.form.getlist("tag_ids")]
        tag_ids = [value for value in tag_ids if value]

        if not company or not title or not description or not requirements or not location:
            flash("Vui lÃ²ng chá»n cÃ´ng ty vÃ  Ä‘iá»n cÃ¡c trÆ°á»ng báº¯t buá»™c.", "error")
            return redirect(url_for("admin.jobs", edit=job_id) if job_id else url_for("admin.jobs"))

        recruiter_user_id = company.recruiter_user_id
        slug_value = slug_value or slugify(title)
        if job:
            slug_conflict = JobPosting.query.filter(JobPosting.slug == slug_value, JobPosting.id != job.id).first()
        else:
            slug_conflict = JobPosting.query.filter_by(slug=slug_value).first()
        if slug_conflict:
            flash("Slug job Ä‘Ã£ tá»“n táº¡i.", "error")
            return redirect(url_for("admin.jobs", edit=job.id if job else None))

        if job:
            job.recruiter_user_id = recruiter_user_id
            job.company_id = company.id
            job.title = title
            job.slug = slug_value
            job.summary = summary
            job.description = description
            job.requirements = requirements
            job.responsibilities = responsibilities
            job.location = location
            job.workplace_type = workplace_type
            job.employment_type = employment_type
            job.experience_level = experience_level
            job.salary_min = salary_min
            job.salary_max = salary_max
            job.salary_currency = salary_currency
            job.vacancy_count = vacancy_count
            job.deadline = deadline
            job.status = status if status in JOB_STATUS_OPTIONS else job.status
            job.is_featured = is_featured
            job.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
            if job.status == "published" and not job.published_at:
                job.published_at = datetime.utcnow()
            _commit("Đã cập nhật job.")
        else:
            job = JobPosting(
                recruiter_user_id=recruiter_user_id,
                company_id=company.id,
                title=title,
                slug=slug_value,
                summary=summary,
                description=description,
                requirements=requirements,
                responsibilities=responsibilities,
                location=location,
                workplace_type=workplace_type,
                employment_type=employment_type,
                experience_level=experience_level,
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency=salary_currency,
                vacancy_count=vacancy_count,
                deadline=deadline,
                status=status if status in JOB_STATUS_OPTIONS else "draft",
                is_featured=is_featured,
                published_at=datetime.utcnow() if status == "published" else None,
            )
            db.session.add(job)
            db.session.flush()
            job.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
            _commit("ÄÃ£ táº¡o job má»›i.")
        return redirect(url_for("admin.jobs"))

    query = JobPosting.query.options(
        joinedload(JobPosting.company).joinedload(Company.recruiter),
        selectinload(JobPosting.tags),
    )
    if filter_q:
        like_q = f"%{filter_q}%"
        query = query.filter(
            or_(
                JobPosting.title.ilike(like_q),
                JobPosting.slug.ilike(like_q),
                JobPosting.location.ilike(like_q),
                JobPosting.summary.ilike(like_q),
                JobPosting.description.ilike(like_q),
            )
        )
    if filter_status in JOB_STATUS_OPTIONS:
        query = query.filter(JobPosting.status == filter_status)
    if filter_company_id:
        query = query.filter(JobPosting.company_id == filter_company_id)
    if filter_tag_id:
        query = query.join(JobPosting.tags).filter(Tag.id == filter_tag_id)
    if filter_featured == "1":
        query = query.filter(JobPosting.is_featured.is_(True))
    elif filter_featured == "0":
        query = query.filter(JobPosting.is_featured.is_(False))

    rows = query.order_by(JobPosting.created_at.desc()).distinct().all()
    return render_template(
        "admin/jobs.html",
        jobs=rows,
        companies=companies,
        tags=tags,
        edit_job=edit_job,
        job_status_options=JOB_STATUS_OPTIONS,
        total_jobs=len(rows),
        filter_q=filter_q,
        filter_status=filter_status,
        filter_company_id=filter_company_id,
        filter_tag_id=filter_tag_id,
        filter_featured=filter_featured,
    )


@admin_bp.route("/applications", methods=["GET", "POST"])
@login_required
@admin_required
def applications():
    edit_id = request.args.get("edit", type=int)
    edit_application = _load_application_or_none(edit_id)

    if request.method == "POST":
        action = request.form.get("action", "save")
        application_id = _to_int(request.form.get("application_id"))
        app_row = _load_application_or_none(application_id)

        if action == "delete" and app_row:
            db.session.delete(app_row)
            _commit("Đã xóa application.")
            return redirect(url_for("admin.applications"))

        if not app_row:
            flash("KhÃ´ng tÃ¬m tháº¥y há»“ sÆ¡ á»©ng tuyá»ƒn.", "error")
            return redirect(url_for("admin.applications"))

        status = request.form.get("status", app_row.status).strip()
        recruiter_note = request.form.get("recruiter_note", "").strip() or None
        app_row.status = status if status in APPLICATION_STATUS_OPTIONS else app_row.status
        app_row.recruiter_note = recruiter_note
        _commit("ÄÃ£ cáº­p nháº­t há»“ sÆ¡ á»©ng tuyá»ƒn.")
        return redirect(url_for("admin.applications"))

    rows = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template(
        "admin/applications.html",
        applications=rows,
        edit_application=edit_application,
        application_status_options=APPLICATION_STATUS_OPTIONS,
        total_applications=len(rows),
    )


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
@admin_required
def categories():
    edit_id = request.args.get("edit", type=int)
    edit_category = _load_category_or_none(edit_id)

    if request.method == "POST":
        action = request.form.get("action", "save")
        category_id = _to_int(request.form.get("category_id"))
        category = _load_category_or_none(category_id)

        if action == "delete" and category:
            db.session.delete(category)
            _commit("Đã xóa category.")
            return redirect(url_for("admin.categories"))

        if action == "toggle" and category:
            category.is_active = not bool(category.is_active)
            _commit("Đã cập nhật trạng thái category.")
            return redirect(url_for("admin.categories"))

        name = request.form.get("name", "").strip()
        slug_value = request.form.get("slug", "").strip()
        description = request.form.get("description", "").strip() or None
        is_active = _to_bool(request.form.get("is_active"))
        slug_value = slug_value or slugify(name)
        if not name:
            flash("TÃªn category lÃ  báº¯t buá»™c.", "error")
            return redirect(url_for("admin.categories", edit=category.id if category else None))

        conflict = Category.query.filter(Category.slug == slug_value, Category.id != (category.id if category else 0)).first()
        if conflict:
            flash("Slug category Ä‘Ã£ tá»“n táº¡i.", "error")
            return redirect(url_for("admin.categories", edit=category.id if category else None))

        if category:
            category.name = name
            category.slug = slug_value
            category.description = description
            category.is_active = is_active
            _commit("Đã cập nhật category.")
        else:
            db.session.add(Category(name=name, slug=slug_value, description=description, is_active=is_active))
            _commit("ÄÃ£ táº¡o category má»›i.")
        return redirect(url_for("admin.categories"))

    rows = Category.query.order_by(Category.name.asc()).all()
    return render_template(
        "admin/categories.html",
        categories=rows,
        edit_category=edit_category,
        total_categories=len(rows),
    )


@admin_bp.route("/tags", methods=["GET", "POST"])
@login_required
@admin_required
def tags():
    edit_id = request.args.get("edit", type=int)
    edit_tag = _load_tag_or_none(edit_id)
    categories = _category_choices()

    if request.method == "POST":
        action = request.form.get("action", "save")
        tag_id = _to_int(request.form.get("tag_id"))
        tag = _load_tag_or_none(tag_id)

        if action == "delete" and tag:
            db.session.delete(tag)
            _commit("Đã xóa tag.")
            return redirect(url_for("admin.tags"))

        if action == "toggle" and tag:
            tag.is_active = not bool(tag.is_active)
            _commit("Đã cập nhật trạng thái tag.")
            return redirect(url_for("admin.tags"))

        name = request.form.get("name", "").strip()
        slug_value = request.form.get("slug", "").strip()
        description = request.form.get("description", "").strip() or None
        category_id = _to_int(request.form.get("category_id"))
        is_active = _to_bool(request.form.get("is_active"))
        category = _load_category_or_none(category_id)

        if not name or not category:
            flash("Vui lòng nhập tên tag và chọn category.", "error")
            return redirect(url_for("admin.tags", edit=tag.id if tag else None))

        slug_value = slug_value or slugify(name)
        conflict = Tag.query.filter(Tag.slug == slug_value, Tag.id != (tag.id if tag else 0)).first()
        if conflict:
            flash("Slug tag Ä‘Ã£ tá»“n táº¡i.", "error")
            return redirect(url_for("admin.tags", edit=tag.id if tag else None))

        if tag:
            tag.name = name
            tag.slug = slug_value
            tag.description = description
            tag.category = category
            tag.is_active = is_active
            _commit("Đã cập nhật tag.")
        else:
            db.session.add(Tag(name=name, slug=slug_value, description=description, category=category, is_active=is_active))
            _commit("ÄÃ£ táº¡o tag má»›i.")
        return redirect(url_for("admin.tags"))

    rows = Tag.query.join(Tag.category).order_by(Category.name.asc(), Tag.name.asc()).all()
    return render_template(
        "admin/tags.html",
        tags=rows,
        categories=categories,
        edit_tag=edit_tag,
        total_tags=len(rows),
    )


@admin_bp.route("/cv-templates", methods=["GET", "POST"])
@login_required
@admin_required
def cv_templates():
    edit_id = request.args.get("edit", type=int)
    edit_template = _load_template_or_none(edit_id)

    if request.method == "POST":
        action = request.form.get("action", "save")
        template_id = _to_int(request.form.get("template_id"))
        template = _load_template_or_none(template_id)

        if action == "delete" and template:
            db.session.delete(template)
            _commit("Đã xóa template CV.")
            return redirect(url_for("admin.cv_templates"))

        if action == "toggle" and template:
            template.is_active = not bool(template.is_active)
            _commit("Đã cập nhật trạng thái template.")
            return redirect(url_for("admin.cv_templates"))

        name = request.form.get("name", "").strip()
        slug_value = request.form.get("slug", "").strip()
        summary = request.form.get("summary", "").strip() or None
        description = request.form.get("description", "").strip() or None
        thumbnail_url = request.form.get("thumbnail_url", "").strip() or None
        preview_url = request.form.get("preview_url", "").strip() or None
        file_format = request.form.get("file_format", "both").strip() or "both"
        is_active = _to_bool(request.form.get("is_active"))
        slug_value = slug_value or slugify(name)

        if not name:
            flash("TÃªn template lÃ  báº¯t buá»™c.", "error")
            return redirect(url_for("admin.cv_templates", edit=template.id if template else None))

        if file_format not in FILE_FORMAT_OPTIONS:
            file_format = "both"

        conflict = CvTemplate.query.filter(CvTemplate.slug == slug_value, CvTemplate.id != (template.id if template else 0)).first()
        if conflict:
            flash("Slug template Ä‘Ã£ tá»“n táº¡i.", "error")
            return redirect(url_for("admin.cv_templates", edit=template.id if template else None))

        if template:
            template.name = name
            template.slug = slug_value
            template.summary = summary
            template.description = description
            template.thumbnail_url = thumbnail_url
            template.preview_url = preview_url
            template.file_format = file_format
            template.is_active = is_active
            _commit("Đã cập nhật template CV.")
        else:
            db.session.add(
                CvTemplate(
                    name=name,
                    slug=slug_value,
                    summary=summary,
                    description=description,
                    thumbnail_url=thumbnail_url,
                    preview_url=preview_url,
                    file_format=file_format,
                    is_active=is_active,
                )
            )
            _commit("ÄÃ£ táº¡o template CV má»›i.")
        return redirect(url_for("admin.cv_templates"))

    rows = CvTemplate.query.order_by(CvTemplate.created_at.desc()).all()
    return render_template(
        "admin/cv_templates.html",
        templates=rows,
        edit_template=edit_template,
        file_format_options=FILE_FORMAT_OPTIONS,
        total_templates=len(rows),
    )
