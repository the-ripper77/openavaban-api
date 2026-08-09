# Random Image

Get one or more random images, optionally filtered by category. No API key required.

## Endpoint

```
GET /api/random
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `category` | string | No | — | Filter by category (partial match) |
| `count` | integer | No | 1 | Number of images (1-25) |

## Response

### Single image (`count=1`)

```json
{
  "id": "64f1a2b3...",
  "name": "Cute Avatar",
  "class_type": "avatar",
  "url": "https://utfs.io/f/...",
  ...
}
```

### Multiple images (`count>1`)

```json
[
  { "id": "...", "name": "...", "url": "..." },
  { "id": "...", "name": "...", "url": "..." }
]
```

## Examples

### Get a random avatar

```bash
curl "https://openavaban-api.giripratik.com.np/api/random?category=avatar"
```

### Get 5 random images

```bash
curl "https://openavaban-api.giripratik.com.np/api/random?count=5"
```

### Get random banner

```bash
curl "https://openavaban-api.giripratik.com.np/api/random?category=banner&count=3"
```

## JavaScript Example

```javascript
// Random image for a profile
async function getRandomAvatar() {
  const res = await fetch('/api/random?category=avatar');
  const image = res.json();
  return image.url;
}
```

## Python Example

```python
import requests

res = requests.get(
    "https://openavaban-api.giripratik.com.np/api/random",
    params={"category": "avatar", "count": 5}
)
images = res.json()

for img in images:
    print(img["url"])
```
