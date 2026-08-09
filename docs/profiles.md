# Get / Update / Delete Profiles

Manage images by image ID or user ID.

---

## Get Images

List images with optional filters.

```
GET /api/profiles
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | No | Get a single image by ID |
| `user_id` | string | No | Filter by user ID |
| `class_type` | string | No | Filter by `avatar` or `banner` |
| `category` | string | No | Filter by category |
| `tags` | string | No | Comma-separated tags (AND logic) |

### Example

```bash
curl "https://openavaban-api.giripratik.com.np/api/profiles?class_type=avatar"
```

### Response

```json
[
  {
    "id": "64f1a2b3...",
    "name": "Profile Photo",
    "class_type": "avatar",
    "category": "profile",
    "url": "https://utfs.io/f/...",
    "tags": ["main"],
    ...
  }
]
```

---

## Get Single Image

```
GET /api/profiles?id=<image_id>
```

```bash
curl "https://openavaban-api.giripratik.com.np/api/profiles?id=64f1a2b3..."
```

---

## Update Image

Update an image's name, tags, category, or metadata.

```
PUT /api/profiles?id=<image_id>
```

### Body (JSON)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | New display name |
| `tags` | array | New tags list |
| `category` | string | New category |
| `class_type` | string | `avatar` or `banner` |
| `metadata` | object | Custom metadata |

### Example

```bash
curl -X PUT "https://openavaban-api.giripratik.com.np/api/profiles?id=64f1a2b3..." \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "tags": ["updated", "v2"]}'
```

### Response

```json
{
  "id": "64f1a2b3...",
  "name": "New Name",
  "tags": ["updated", "v2"],
  ...
}
```

---

## Delete Image

Delete an image from the database and UploadThing.

```
DELETE /api/profiles?id=<image_id>
```

### Example

```bash
curl -X DELETE "https://openavaban-api.giripratik.com.np/api/profiles?id=64f1a2b3..."
```

### Response

```json
{
  "success": true,
  "deleted": "64f1a2b3..."
}
```

---

## Error Responses

| Status | Error | Cause |
|--------|-------|-------|
| 400 | `id parameter is required` | Missing id in PUT/DELETE |
| 404 | `Image not found` | Image doesn't exist |
