# Bulk Upload

Upload up to 100 images at once using a CSV file.

## How It Works

1. Download the CSV template
2. Fill in each row with an image URL and metadata
3. Upload the CSV to the bulk upload page
4. All images are processed and added to your gallery

## CSV Format

| Column | Required | Description |
|--------|----------|-------------|
| `file_url` | Yes | Direct URL to the image file |
| `name` | Yes | Display name |
| `class_type` | Yes | `avatar` or `banner` |
| `category` | No | Category string |
| `tags` | No | Comma-separated tags |

## Template

Download the template from the [bulk upload page](https://openavaban-api.giripratik.com.np/bulk).

Example content:

```csv
file_url,name,class_type,category,tags
https://example.com/photo1.jpg,Profile Photo,avatar,profile,"main,profile"
https://example.com/banner1.png,Social Banner,banner,social,"banner,v2"
https://example.com/photo2.png,Cute Avatar,avatar,profile,cute
```

## Limits

- Maximum **100 rows** per CSV
- Image files must be **10 MB** or smaller
- Supported formats: **JPG, PNG, GIF, WebP**
- Images must be accessible via direct URL

## Upload Page

Go to [openavaban-api.giripratik.com.np/bulk](https://openavaban-api.giripratik.com.np/bulk) to use the bulk upload form.

## API Endpoint

```
POST /api/bulk
```

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Content-Type` | Yes | `multipart/form-data` |

### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | CSV file | Yes | CSV with image URLs and metadata |

### Response

```json
{
  "total": 50,
  "success": 48,
  "failed": 2,
  "results": [
    {"row": 1, "status": "ok", "url": "https://utfs.io/f/..."},
    {"row": 12, "status": "error", "error": "Failed to download image"},
    {"row": 37, "status": "error", "error": "Invalid file type"}
  ]
}
```

## Python Example

```python
import requests

files = {"file": open("images.csv", "rb")}

res = requests.post(
    "https://openavaban-api.giripratik.com.np/api/bulk",
    files=files
)
print(res.json())
```

## JavaScript Example

```javascript
const form = new FormData();
form.append("file", csvInput.files[0]);

const res = await fetch("/api/bulk", {
  method: "POST",
  body: form
});
const data = await res.json();
console.log(`${data.success} uploaded, ${data.failed} failed`);
```
