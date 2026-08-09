# openavaban-api

REST API for managing profile avatars and banners with a public gallery.

## Features

- Image upload (avatars, banners)
- Public home page with masonry grid
- Full-text search with MIME type filters (JPG, PNG, GIF, WebP)
- Random image endpoint
- Bulk upload via CSV (up to 100 images)
- CRUD operations

## Links

- **Home**: [openavaban-api.giripratik.com.np](https://openavaban-api.giripratik.com.np/)
- **Docs**: [openavaban-api.giripratik.com.np/docs/about](https://openavaban-api.giripratik.com.np/docs/about)
- **Bulk Upload**: [openavaban-api.giripratik.com.np/bulk](https://openavaban-api.giripratik.com.np/bulk)
- **Python Library**: [pypi.org/project/openavaban](https://pypi.org/project/openavaban/)
- **Source Code**: [github.com/the-ripper77/openavaban-api](https://github.com/the-ripper77/openavaban-api)

## Quick Start

```bash
pip install openavaban
```

```python
from openavaban import OpenavaBan

client = OpenavaBan()

# Upload
result = client.upload(
    file="photo.jpg",
    name="Profile Photo",
    class_type="avatar",
    user_id="user_123"
)

# Get user's images
images = client.get_all(user_id="user_123")
```

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/search?q=&class_type=&mime_type=` | No | Search images |
| `GET` | `/api/random?category=&count=` | No | Random image(s) |
| `POST` | `/api/upload` | Yes | Upload image |
| `GET` | `/api/profiles?user_id=` | Yes | List user images |
| `PUT` | `/api/profiles?id=` | Yes | Update image |
| `DELETE` | `/api/profiles?id=` | Yes | Delete image |
| `POST` | `/api/bulk` | Yes | Bulk upload via CSV |

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home — masonry grid gallery with search |
| `/bulk` | Bulk upload — CSV upload with template |
| `/docs/about` | Documentation |

## Documentation

Full API docs at [openavaban-api.giripratik.com.np/docs/about](https://openavaban-api.giripratik.com.np/docs/about)

- [About](https://openavaban-api.giripratik.com.np/docs/about)
- [Quick Start](https://openavaban-api.giripratik.com.np/docs/quickstart)
- [Search Images](https://openavaban-api.giripratik.com.np/docs/search)
- [Upload Image](https://openavaban-api.giripratik.com.np/docs/upload)
- [Get / Update / Delete](https://openavaban-api.giripratik.com.np/docs/profiles)
- [Random Image](https://openavaban-api.giripratik.com.np/docs/random)
- [Bulk Upload](https://openavaban-api.giripratik.com.np/docs/bulk-upload)

## License

MIT
