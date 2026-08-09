# Search Images

Search for images across name, tags, category, and user ID. No API key required.

## Endpoint

```
GET /api/search
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | No | — | Search query (searches name, tags, category, user_id) |
| `class_type` | string | No | — | Filter by `avatar` or `banner` |
| `category` | string | No | — | Filter by category (partial match) |
| `tags` | string | No | — | Comma-separated tags (AND logic) |
| `limit` | integer | No | 30 | Max results (1-100) |
| `offset` | integer | No | 0 | Skip N results for pagination |

## Response

```json
{
  "total": 42,
  "offset": 0,
  "limit": 30,
  "has_more": true,
  "results": [
    {
      "id": "64f1a2b3...",
      "name": "Profile Photo",
      "class_type": "avatar",
      "category": "profile",
      "url": "https://utfs.io/f/...",
      "key": "...",
      "user_id": "user_123",
      "created_at": "2026-08-09T10:00:00+00:00",
      "updated_at": "2026-08-09T10:00:00+00:00",
      "file_size": 102400,
      "mime_type": "image/jpeg",
      "tags": ["main", "profile"],
      "metadata": {},
      "dimensions": { "width": 800, "height": 600 }
    }
  ]
}
```

## Examples

### Search by keyword

```bash
curl "https://openavaban-api.giripratik.com.np/api/search?q=cute"
```

### Filter by type

```bash
curl "https://openavaban-api.giripratik.com.np/api/search?class_type=avatar"
```

### Search with tags

```bash
curl "https://openavaban-api.giripratik.com.np/api/search?tags=main,profile"
```

### Pagination

```bash
# Page 1
curl "https://openavaban-api.giripratik.com.np/api/search?limit=10&offset=0"

# Page 2
curl "https://openavaban-api.giripratik.com.np/api/search?limit=10&offset=10"
```

### Combined filters

```bash
curl "https://openavaban-api.giripratik.com.np/api/search?q=anime&class_type=banner&limit=5"
```

## JavaScript Example

```javascript
const res = await fetch('/api/search?q=cute&limit=10');
const data = await res.json();

data.results.forEach(image => {
  console.log(image.name, image.url);
});
```

## Python Example

```python
import requests

res = requests.get(
    "https://openavaban-api.giripratik.com.np/api/search",
    params={"q": "cute", "limit": 10}
)
data = res.json()

for image in data["results"]:
    print(image["name"], image["url"])
```
