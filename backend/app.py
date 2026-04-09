from pathlib import Path
from urllib.parse import urlparse
from flask import Flask, redirect, url_for
from sqlalchemy import inspect, text

from .api.registry import register_api_blueprints
from .core.config import Config
from .core.extensions import cors, db, jwt, login_manager, mail, migrate
from .core.seed import seed_initial_data
from .repositories import get_user_by_id
from .web.registry import register_web_blueprints


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    frontend_origins = _build_frontend_origins(app.config["FRONTEND_URL"])
    cors.init_app(app, resources={r"/api/*": {"origins": frontend_origins}}, supports_credentials=True)
    login_manager.login_view = "admin.login"

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(int(user_id))

    register_api_blueprints(app)
    register_web_blueprints(app)

    @app.route("/")
    def index():
        return redirect(url_for("admin.login"))

    with app.app_context():
        Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
        db.create_all()
        _ensure_otp_schema()
        if app.config["SEED_DATA"]:
            seed_initial_data()

    return app


def _build_frontend_origins(primary_origin):
    origins = {primary_origin}
    parsed = urlparse(primary_origin)
    if parsed.scheme and parsed.hostname in {"127.0.0.1", "localhost"}:
        host_variants = {"127.0.0.1", "localhost"}
        for host in host_variants:
            origins.add(f"{parsed.scheme}://{host}:{parsed.port or 5173}")
    return sorted(origins)


def _ensure_otp_schema():
    inspector = inspect(db.engine)
    if "otp_codes" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("otp_codes")}
    statements = []
    if "resend_available_at" not in columns:
        statements.append(
            "ALTER TABLE otp_codes ADD COLUMN resend_available_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
        )
    if "max_attempts" not in columns:
        statements.append("ALTER TABLE otp_codes ADD COLUMN max_attempts INT NOT NULL DEFAULT 5")
    if "request_ip" not in columns:
        statements.append("ALTER TABLE otp_codes ADD COLUMN request_ip VARCHAR(64)")

    for statement in statements:
        db.session.execute(text(statement))
    if statements:
        db.session.commit()
