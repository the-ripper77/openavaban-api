from datetime import datetime, timezone


VALID_CLASS_TYPES = ("avatar", "banner")

VALID_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_class_type(class_type: str):
    if class_type not in VALID_CLASS_TYPES:
        raise ValueError(
            f"Invalid class_type '{class_type}'. Must be one of: {', '.join(VALID_CLASS_TYPES)}"
        )


def validate_mime_type(mime_type: str):
    if mime_type not in VALID_IMAGE_TYPES:
        raise ValueError(
            f"Invalid file type '{mime_type}'. Allowed: {', '.join(VALID_IMAGE_TYPES)}"
        )


def validate_file_size(size: int):
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File too large: {size} bytes. Max: {MAX_FILE_SIZE} bytes ({MAX_FILE_SIZE // (1024*1024)} MB)"
        )


def create_document(
    name: str,
    class_type: str,
    url: str,
    key: str,
    file_size: int,
    mime_type: str,
    user_id: str,
    category: str = "",
    tags: list = None,
    metadata: dict = None,
    dimensions: dict = None,
) -> dict:
    validate_class_type(class_type)
    validate_mime_type(mime_type)
    validate_file_size(file_size)

    now = datetime.now(timezone.utc)

    doc = {
        "name": name,
        "class_type": class_type,
        "category": category,
        "url": url,
        "key": key,
        "user_id": user_id,
        "created_at": now,
        "updated_at": now,
        "file_size": file_size,
        "mime_type": mime_type,
        "tags": tags or [],
        "metadata": metadata or {},
    }

    if dimensions:
        doc["dimensions"] = {
            "width": dimensions.get("width", 0),
            "height": dimensions.get("height", 0),
        }
    else:
        doc["dimensions"] = {"width": 0, "height": 0}

    return doc


def to_response(doc: dict) -> dict:
    if doc is None:
        return None

    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "class_type": doc["class_type"],
        "category": doc["category"],
        "url": doc["url"],
        "key": doc["key"],
        "user_id": doc["user_id"],
        "created_at": doc["created_at"].isoformat() if doc.get("created_at") else None,
        "updated_at": doc["updated_at"].isoformat() if doc.get("updated_at") else None,
        "file_size": doc["file_size"],
        "mime_type": doc["mime_type"],
        "tags": doc["tags"],
        "metadata": doc["metadata"],
        "dimensions": doc["dimensions"],
    }
