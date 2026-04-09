from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cloudinary
import cloudinary.uploader
from flask import current_app


@dataclass
class UploadResult:
    url: str
    public_id: str
    resource_type: str


def init_cloudinary() -> bool:
    cloud_name = current_app.config.get("CLOUDINARY_CLOUD_NAME")
    api_key = current_app.config.get("CLOUDINARY_API_KEY")
    api_secret = current_app.config.get("CLOUDINARY_API_SECRET")
    if not (cloud_name and api_key and api_secret):
        return False
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )
    return True


def upload_image(file_storage: Any, folder: str, public_id: str | None = None) -> UploadResult | None:
    if file_storage is None:
        return None
    if not init_cloudinary():
        return None
    options = {
        "folder": folder,
        "resource_type": "image",
        "overwrite": True,
        "use_filename": True,
        "unique_filename": True,
    }
    if public_id:
        options["public_id"] = public_id
    result = cloudinary.uploader.upload(file_storage, **options)
    return UploadResult(
        url=result.get("secure_url", ""),
        public_id=result.get("public_id", ""),
        resource_type=result.get("resource_type", "image"),
    )
