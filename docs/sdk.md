# Python SDK

Install the `openavaban` Python package to interact with the API without writing raw HTTP requests.

## Installation

```bash
pip install openavaban
```

## Quick Start

```python
from openavaban import OpenavaBan

client = OpenavaBan()  # uses hosted API

# Upload
result = client.upload("photo.jpg", name="Profile Photo", class_type="avatar")
print(result["url"])

# Search
results = client.search(class_type="avatar")
for img in results["results"]:
    print(img["name"], img["url"])

# Random
random_imgs = client.random(count=5)
```

No API keys or database credentials needed.

## Methods

### Upload Image

```python
result = client.upload(
    file="photo.jpg",          # file path or file-like object
    name="Profile Photo",      # display name
    class_type="avatar",       # "avatar" or "banner"
    category="profile",        # optional category
    tags=["main", "profile"],  # optional tags list
    metadata={"source": "web"} # optional metadata dict
)
```

Returns:

```python
{
    "id": "64f1a2b3...",
    "name": "Profile Photo",
    "class_type": "avatar",
    "category": "profile",
    "url": "https://utfs.io/f/...",
    "tags": ["main", "profile"],
    "created_at": "2026-08-09T10:00:00+00:00",
    ...
}
```

### Bulk Upload

```python
result = client.bulk_upload("images.csv")
print(f"Uploaded {result['success']}/{result['total']}")
```

CSV format:

```csv
file_url,name,class_type,category,tags
https://example.com/photo1.jpg,Profile Photo,avatar,profile,"main,profile"
https://example.com/banner1.png,Social Banner,banner,social,"banner,v2"
```

### Search Images

```python
results = client.search(
    q="profile",           # search across name, tags, category
    class_type="avatar",   # filter by type
    category="profile",    # filter by category
    tags=["main"],         # filter by tags (AND)
    mime_type="gif",       # "image" or "gif"
    limit=30,              # max 100
    offset=0               # pagination
)
```

Returns:

```python
{
    "total": 42,
    "offset": 0,
    "limit": 30,
    "has_more": True,
    "results": [...]
}
```

### Random Images

```python
result = client.random(category="profile", count=5)
# Returns {"images": [...]}
```

### Get by ID

```python
image = client.get("image_id_here")
```

### Update

```python
client.update("image_id_here", name="New Name", tags=["updated", "v2"])
```

### Delete

```python
client.delete("image_id_here")
```

## Custom API URL

Point to a different API instance:

```python
client = OpenavaBan(base_url="http://localhost:3000")
```

## Exceptions

| Exception | Description |
|---|---|
| `APIError` | API request failed |
| `InvalidClassError` | Invalid class_type |
| `NotFoundError` | Image not found |
| `ValidationError` | Invalid file or missing fields |

```python
from openavaban import OpenavaBan, NotFoundError

client = OpenavaBan()
try:
    image = client.get("nonexistent_id")
except NotFoundError:
    print("Image not found")
```
