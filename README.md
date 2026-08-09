# openavaban-api

REST API for managing profile avatars and banners via UploadThing and MongoDB.

## Endpoints

### Upload Image

```
POST /api/upload
```

**Headers:**
- `X-API-Key: your-api-key`
- `Content-Type: multipart/form-data`

**Form Fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `file` | Yes | Image file (jpg, png, gif, webp) |
| `name` | Yes | Display name |
| `class_type` | Yes | `avatar` or `banner` |
| `user_id` | Yes | User identifier |
| `category` | No | Category string |
| `tags` | No | Comma-separated tags |
| `metadata` | No | JSON string |

**Max file size:** 10 MB

**Response:** `201 Created`
```json
{
    "id": "64f1a2b3...",
    "name": "Profile Photo",
    "class_type": "avatar",
    "category": "profile",
    "url": "https://utfs.io/f/...",
    "user_id": "user_123",
    "created_at": "2026-08-09T10:00:00+00:00",
    "file_size": 102400,
    "mime_type": "image/jpeg",
    "tags": ["main"],
    "metadata": {},
    "dimensions": {"width": 800, "height": 600}
}
```

---

### List User Images

```
GET /api/profiles?user_id=xxx&class_type=avatar&category=profile&tags=main,profile
```

**Headers:**
- `X-API-Key: your-api-key`

**Query Parameters:**
| Param | Required | Description |
|-------|----------|-------------|
| `user_id` | Yes | User identifier |
| `class_type` | No | Filter by `avatar` or `banner` |
| `category` | No | Filter by category |
| `tags` | No | Comma-separated tags (AND logic) |

**Response:** `200 OK`
```json
[
    {
        "id": "64f1a2b3...",
        "name": "Profile Photo",
        "class_type": "avatar",
        "url": "https://...",
        ...
    }
]
```

---

### Get Single Image

```
GET /api/profiles/:id
```

**Headers:**
- `X-API-Key: your-api-key`

**Response:** `200 OK`
```json
{
    "id": "64f1a2b3...",
    "name": "Profile Photo",
    "class_type": "avatar",
    "url": "https://...",
    ...
}
```

---

### Update Image

```
PUT /api/profiles/:id
```

**Headers:**
- `X-API-Key: your-api-key`
- `Content-Type: application/json`

**Body:**
```json
{
    "name": "New Name",
    "tags": ["updated", "v2"],
    "category": "social"
}
```

**Allowed fields:** `name`, `category`, `tags`, `metadata`, `class_type`

**Response:** `200 OK`
```json
{
    "id": "64f1a2b3...",
    "name": "New Name",
    ...
}
```

---

### Delete Image

```
DELETE /api/profiles/:id
```

**Headers:**
- `X-API-Key: your-api-key`

**Response:** `200 OK`
```json
{
    "success": true,
    "deleted": "64f1a2b3..."
}
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGODB_URI` | MongoDB connection string |
| `UPLOADTHING_TOKEN` | UploadThing v7 token |
| `API_KEY` | API authentication key |

## Deploy to Vercel

```bash
npm i -g vercel
cd D:\upava-api
vercel
```

Then set environment variables in Vercel dashboard.
