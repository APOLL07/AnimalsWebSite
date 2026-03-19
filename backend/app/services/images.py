"""Image and video upload and processing service."""

import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.config import settings

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
SIZES = {
    "thumb": (200, 200),
    "medium": (600, 600),
    "large": (1200, 1200),
}


def _ensure_dirs() -> Path:
    base = Path(settings.UPLOAD_DIR)
    for size_name in SIZES:
        (base / size_name).mkdir(parents=True, exist_ok=True)
    return base


async def save_upload(file: UploadFile) -> dict[str, str]:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип файла: {file.content_type}",
        )

    data = await file.read()
    if len(data) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл слишком большой (макс. 5 МБ)",
        )

    base_dir = _ensure_dirs()
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.webp"

    from io import BytesIO
    img = Image.open(BytesIO(data))
    if img.mode in ("RGBA", "P", "LA", "PA"):
        img = img.convert("RGB")

    urls = {}
    for size_name, max_size in SIZES.items():
        resized = img.copy()
        resized.thumbnail(max_size, Image.LANCZOS)
        out_path = base_dir / size_name / filename
        resized.save(out_path, "WEBP", quality=85)
        urls[size_name] = f"/media/{size_name}/{filename}"

    return urls


async def save_video_upload(file: UploadFile) -> str:
    """Save a video file without processing. Returns the URL path."""
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип видео: {file.content_type}",
        )

    data = await file.read()
    if len(data) > MAX_VIDEO_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Видео слишком большое (макс. 50 МБ)",
        )

    base_dir = Path(settings.UPLOAD_DIR)
    videos_dir = base_dir / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)

    ext = "mp4"
    if file.content_type == "video/webm":
        ext = "webm"
    elif file.content_type == "video/quicktime":
        ext = "mov"

    file_id = str(uuid.uuid4())
    filename = f"{file_id}.{ext}"
    out_path = videos_dir / filename

    with open(out_path, "wb") as f:
        f.write(data)

    return f"/media/videos/{filename}"


def delete_video_file(url: str) -> None:
    """Delete a video file from disk."""
    base_dir = Path(settings.UPLOAD_DIR)
    filename = url.split("/")[-1]
    path = base_dir / "videos" / filename
    if path.exists():
        path.unlink()


def delete_image_files(url: str) -> None:
    base_dir = Path(settings.UPLOAD_DIR)
    filename = url.split("/")[-1]
    for size_name in SIZES:
        path = base_dir / size_name / filename
        if path.exists():
            path.unlink()
