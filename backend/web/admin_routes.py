from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..core.extensions import db
from ..core.security import slugify, verify_password
from ..models import Application, Category, Company, JobPosting, Tag, User

admin_bp = Blueprint("admin", __name__, template_folder="../templates")


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            return redirect(url_for("admin.login"))
        return fn(*args, **kwargs)

    return wrapper


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
        flash("Sai tài khoản hoặc mật khẩu admin.", "danger")
    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "users": User.query.count(),
        "admins": User.query.filter_by(role="admin").count(),
        "recruiters": User.query.filter_by(role="recruiter").count(),
        "candidates": User.query.filter_by(role="candidate").count(),
        "jobs": JobPosting.query.count(),
        "companies": Company.query.count(),
        "applications": Application.query.count(),
        "categories": Category.query.count(),
        "tags": Tag.query.count(),
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = JobPosting.query.order_by(JobPosting.created_at.desc()).limit(5).all()
    recent_apps = Application.query.order_by(Application.applied_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_users=recent_users,
        recent_jobs=recent_jobs,
        recent_apps=recent_apps,
    )


@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@admin_required
def users():
    if request.method == "POST":
        action = request.form.get("action")
        user = User.query.get(int(request.form.get("user_id")))
        if user and action == "toggle":
            user.status = "locked" if user.status == "active" else "active"
            db.session.commit()
            flash("Đã cập nhật trạng thái tài khoản.", "success")
        return redirect(url_for("admin.users"))
    rows = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=rows)


@admin_bp.route("/companies", methods=["GET", "POST"])
@login_required
@admin_required
def companies():
    if request.method == "POST":
        company = Company(
            recruiter_user_id=int(request.form.get("recruiter_user_id")),
            company_name=request.form.get("company_name"),
            tax_code=request.form.get("tax_code"),
            website=request.form.get("website"),
            address=request.form.get("address"),
            description=request.form.get("description"),
            logo_url=request.form.get("logo_url"),
            industry=request.form.get("industry"),
        )
        db.session.add(company)
        db.session.commit()
        flash("Đã thêm company.", "success")
        return redirect(url_for("admin.companies"))
    rows = Company.query.order_by(Company.created_at.desc()).all()
    recruiters = User.query.filter_by(role="recruiter").all()
    return render_template("admin/companies.html", companies=rows, recruiters=recruiters)


@admin_bp.route("/jobs", methods=["GET", "POST"])
@login_required
@admin_required
def jobs():
    if request.method == "POST":
        job = JobPosting.query.get(int(request.form.get("job_id")))
        if job:
            job.status = request.form.get("status", job.status)
            db.session.commit()
            flash("Đã cập nhật job.", "success")
        return redirect(url_for("admin.jobs"))
    rows = JobPosting.query.order_by(JobPosting.created_at.desc()).all()
    return render_template("admin/jobs.html", jobs=rows)


@admin_bp.route("/applications", methods=["GET", "POST"])
@login_required
@admin_required
def applications():
    if request.method == "POST":
        app_row = Application.query.get(int(request.form.get("application_id")))
        if app_row:
            app_row.status = request.form.get("status", app_row.status)
            db.session.commit()
            flash("Đã cập nhật hồ sơ.", "success")
        return redirect(url_for("admin.applications"))
    rows = Application.query.order_by(Application.applied_at.desc()).all()
    return render_template("admin/applications.html", applications=rows)


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
@admin_required
def categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        if name:
            slug = slugify(name)
            category = Category.query.filter_by(slug=slug).first()
            if not category:
                category = Category(name=name, slug=slug, description=description)
                db.session.add(category)
            else:
                category.name = name
                category.description = description
                category.is_active = True
            db.session.commit()
            flash("Đã thêm category.", "success")
        return redirect(url_for("admin.categories"))
    rows = Category.query.order_by(Category.name.asc()).all()
    return render_template("admin/categories.html", categories=rows)


@admin_bp.route("/tags", methods=["GET", "POST"])
@login_required
@admin_required
def tags():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category_id = request.form.get("category_id", "").strip()
        category = db.session.get(Category, int(category_id)) if category_id else None
        if name and category:
            tag = Tag.query.filter_by(slug=slugify(name)).first()
            if not tag:
                tag = Tag(name=name, slug=slugify(name), category=category, description=request.form.get("description"))
                db.session.add(tag)
            else:
                tag.name = name
                tag.category = category
                tag.description = request.form.get("description")
                tag.is_active = True
            db.session.commit()
            flash("Đã thêm tag.", "success")
        return redirect(url_for("admin.tags"))
    rows = Tag.query.join(Tag.category).order_by(Category.name.asc(), Tag.name.asc()).all()
    categories_rows = Category.query.order_by(Category.name.asc()).all()
    return render_template("admin/tags.html", tags=rows, categories=categories_rows)
