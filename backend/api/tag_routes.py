from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import json_error, json_ok, role_required
from ..core.extensions import db
from ..models import Category, Tag
from ..core.security import slugify
from ..repositories import list_active_categories, list_active_tags
from ..schemas import category_to_dict, tag_to_dict

api_tags_bp = Blueprint("api_tags", __name__)


@api_tags_bp.get("")
def list_tags():
    category = request.args.get("category")
    tags = list_active_tags(category)
    return json_ok([tag_to_dict(tag) for tag in tags])


@api_tags_bp.get("/categories")
def list_categories():
    categories = list_active_categories()
    return json_ok([category_to_dict(category) for category in categories])


@api_tags_bp.post("")
@jwt_required()
@role_required("admin")
def create_tag():
    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    category_id = data.get("category_id")
    category_slug = data.get("category") or data.get("category_slug")
    category = None
    if category_id:
        category = db.session.get(Category, int(category_id))
    elif category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
    if not name or not category:
        return json_error("name and category are required.", 400)
    tag = Tag(name=name, slug=slugify(name), category=category, description=data.get("description"))
    db.session.add(tag)
    db.session.commit()
    return json_ok(tag_to_dict(tag), "Tag created", 201)


@api_tags_bp.put("/<int:tag_id>")
@api_tags_bp.patch("/<int:tag_id>")
@jwt_required()
@role_required("admin")
def update_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return json_error("Tag not found.", 404)
    data = request.get_json(force=True)
    for field in ["name", "description", "is_active"]:
        if field in data:
            setattr(tag, field, data[field])
    if "name" in data:
        tag.slug = slugify(data["name"])
    if "category_id" in data and data["category_id"]:
        tag.category = db.session.get(Category, int(data["category_id"]))
    elif "category" in data or "category_slug" in data:
        category_slug = data.get("category") or data.get("category_slug")
        if category_slug:
            tag.category = Category.query.filter_by(slug=category_slug).first()
    db.session.commit()
    return json_ok(tag_to_dict(tag))


@api_tags_bp.delete("/<int:tag_id>")
@jwt_required()
@role_required("admin")
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return json_error("Tag not found.", 404)
    db.session.delete(tag)
    db.session.commit()
    return json_ok(message="Tag deleted")
