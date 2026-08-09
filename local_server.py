import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from api.docs import render_page, PAGES
from lib.mongodb import get_collection
from lib.models import to_response

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class TestHandler(BaseHTTPRequestHandler):
    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/" or path == "":
            html_path = os.path.join(STATIC_DIR, "index.html")
            with open(html_path, "rb") as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html)

        elif path == "/bulk":
            html_path = os.path.join(STATIC_DIR, "bulk.html")
            with open(html_path, "rb") as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html)

        elif path.startswith("/docs"):
            slug = path.strip("/").split("/")[-1] if path.strip("/") else "about"
            slug = slug or "about"
            valid_slugs = [p["slug"] for p in PAGES]
            if slug not in valid_slugs:
                slug = "about"
            html = render_page(slug)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

        elif path == "/api/search":
            try:
                collection = get_collection()
                query_text = params.get("q", [None])[0]
                class_type = params.get("class_type", [None])[0]
                category = params.get("category", [None])[0]
                tags = params.get("tags", [None])[0]
                mime_type = params.get("mime_type", [None])[0]
                limit = min(int(params.get("limit", [30])[0]), 100)
                offset = int(params.get("offset", [0])[0])

                query = {}
                if class_type:
                    query["class_type"] = class_type
                if mime_type:
                    if mime_type == "image":
                        query["mime_type"] = {"$in": ["image/jpeg", "image/png", "image/webp"]}
                    elif mime_type == "gif":
                        query["mime_type"] = "image/gif"
                if category:
                    query["category"] = {"$regex": category, "$options": "i"}
                if tags:
                    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
                    if tag_list:
                        query["tags"] = {"$all": tag_list}
                if query_text:
                    regex = {"$regex": query_text, "$options": "i"}
                    query["$or"] = [
                        {"name": regex},
                        {"tags": regex},
                        {"category": regex},
                        {"user_id": regex},
                    ]

                total = collection.count_documents(query)
                docs = list(collection.find(query).sort("created_at", -1).skip(offset).limit(limit))
                results = [to_response(doc) for doc in docs]

                self._json_response(200, {
                    "total": total,
                    "offset": offset,
                    "limit": limit,
                    "has_more": (offset + limit) < total,
                    "results": results,
                })
            except Exception as e:
                self._json_response(500, {"error": str(e)})

        elif path == "/api/random":
            try:
                collection = get_collection()
                category = params.get("category", [None])[0]
                count = min(int(params.get("count", [1])[0]), 25)
                query = {}
                if category:
                    query["category"] = {"$regex": category, "$options": "i"}
                total = collection.count_documents(query)
                if total == 0:
                    self._json_response(200, {"error": "No images found"})
                    return
                pipeline = [{"$match": query}, {"$sample": {"size": count}}]
                docs = list(collection.aggregate(pipeline))
                results = [to_response(doc) for doc in docs]
                self._json_response(200, results[0] if count == 1 else results)
            except Exception as e:
                self._json_response(500, {"error": str(e)})

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/bulk":
            from api.bulk_process import handler as BulkHandler
            BulkHandler.do_POST(self)
        elif path == "/api/upload":
            from api.upload import handler as UploadHandler
            UploadHandler.do_POST(self)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def _parse_multipart(self, body, boundary):
        parts = {}
        boundary_bytes = boundary.encode()
        splits = body.split(b"--" + boundary_bytes)

        for part in splits[1:]:
            if part.strip() == b"" or part.strip() == b"--":
                continue

            header_end = part.find(b"\r\n\r\n")
            if header_end == -1:
                continue

            headers_raw = part[:header_end].decode()
            data = part[header_end + 4:]
            if data.endswith(b"\r\n"):
                data = data[:-2]

            name = None
            filename = None
            content_type = None

            for line in headers_raw.split("\r\n"):
                if "Content-Disposition:" in line:
                    for segment in line.split(";"):
                        segment = segment.strip()
                        if segment.startswith("name="):
                            name = segment.split("=")[1].strip('"')
                        elif segment.startswith("filename="):
                            filename = segment.split("=")[1].strip('"')
                elif "Content-Type:" in line:
                    content_type = line.split(":")[1].strip()

            if name:
                parts[name] = {
                    "data": data,
                    "filename": filename,
                    "content_type": content_type or "application/octet-stream",
                }

        return parts

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/profiles":
            from api.profiles import handler as ProfilesHandler
            ProfilesHandler.do_PUT(self)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/profiles":
            from api.profiles import handler as ProfilesHandler
            ProfilesHandler.do_DELETE(self)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")


if __name__ == "__main__":
    port = 3000
    server = HTTPServer(("127.0.0.1", port), TestHandler)
    print(f"openavaban-api running at http://localhost:{port}")
    print("  Home:     http://localhost:3000/")
    print("  Bulk:     http://localhost:3000/bulk")
    print("  Docs:     http://localhost:3000/docs/about")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()
