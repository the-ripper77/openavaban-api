# Quick Start

Make your first API call in 2 minutes.

## 1. Browse the Gallery

Visit [openavaban-api.giripratik.com.np](https://openavaban-api.giripratik.com.np/) to see all uploaded images in a searchable grid.

## 2. Search for Images

```bash
curl "https://openavaban-api.giripratik.com.np/api/search?q=cute"
```

## 3. Get a Random Image

```bash
curl "https://openavaban-api.giripratik.com.np/api/random"
```

## 4. Upload an Image

```bash
curl -X POST "https://openavaban-api.giripratik.com.np/api/upload" \
  -H "X-API-Key: your-api-key" \
  -F "file=@photo.jpg" \
  -F "name=Profile Photo" \
  -F "class_type=avatar" \
  -F "user_id=user_123"
```

## 5. Python Library

```bash
pip install openavaban
```

```python
from openavaban import OpenavaBan

client = OpenavaBan()

# Get all avatars
images = client.get_all(user_id="user_123")

# Upload a new avatar
result = client.upload(
    file="photo.jpg",
    name="Profile Photo",
    class_type="avatar",
    user_id="user_123"
)
```

## Next Steps

- [Search Images](/docs/search) — Full-text search with filters
- [Upload Image](/docs/upload) — Upload with metadata
- [Bulk Upload](/docs/bulk-upload) — Upload 100 images at once via CSV
- [API Reference](/docs/profiles) — Get, update, delete images
