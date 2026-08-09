# Upload Image

Upload an image (avatar or banner) with metadata.

## Endpoint

```
POST /api/upload
```

## Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `multipart/form-data` |

## Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Image file (jpg, png, gif, webp). Max 10 MB |
| `name` | string | Yes | Display name for the image |
| `class_type` | string | Yes | `avatar` or `banner` |
| `user_id` | string | No | User identifier |
| `category` | string | No | Category string (e.g., "profile", "social") |
| `tags` | string | No | Comma-separated tags (e.g., "main,profile") |
| `metadata` | string | No | JSON string of custom metadata |

## Response

```json
{
  "id": "64f1a2b3...",
  "name": "Profile Photo",
  "class_type": "avatar",
  "category": "profile",
  "url": "https://utfs.io/f/...",
  "key": "...",
  "user_id": "",
  "created_at": "2026-08-09T10:00:00+00:00",
  "updated_at": "2026-08-09T10:00:00+00:00",
  "file_size": 102400,
  "mime_type": "image/jpeg",
  "tags": ["main", "profile"],
  "metadata": {},
  "dimensions": { "width": 800, "height": 600 }
}
```

## Examples

### curl

```bash
curl -X POST "https://openavaban-api.giripratik.com.np/api/upload" \
  -F "file=@photo.jpg" \
  -F "name=Profile Photo" \
  -F "class_type=avatar" \
  -F "category=profile" \
  -F "tags=main,profile"
```

### Python

```python
import requests

res = requests.post(
    "https://openavaban-api.giripratik.com.np/api/upload",
    files={"file": open("photo.jpg", "rb")},
    data={
        "name": "Profile Photo",
        "class_type": "avatar",
        "category": "profile",
        "tags": "main,profile"
    }
)
print(res.json())
```

### JavaScript

```javascript
const form = new FormData();
form.append("file", fileInput.files[0]);
form.append("name", "Profile Photo");
form.append("class_type", "avatar");

const res = await fetch("/api/upload", {
  method: "POST",
  body: form
});
const data = await res.json();
console.log(data.url);
```

## Error Responses

| Status | Error | Cause |
|--------|-------|-------|
| 400 | `Content-Type must be multipart/form-data` | Wrong content type |
| 400 | `No file provided` | Missing file field |
| 400 | `name and class_type are required` | Missing required fields |
| 413 | `File too large: ... bytes. Max: 10485760 bytes` | File exceeds 10 MB |
