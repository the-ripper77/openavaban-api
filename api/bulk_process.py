import json
import os
import sys
import csv
import io
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.mongodb import get_collection
from lib.models import create_document

MAX_ROWS = 100


class handler(BaseHTTPRequestHandler):
    def _json_response(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._json_response(400, {"error": "Content-Type must be multipart/form-data"})
            return

        try:
            boundary = content_type.split("boundary=")[1]
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            parts = self._parse_multipart(body, boundary)

            csv_data = parts.get("file", {}).get("data")
            if not csv_data:
                self._json_response(400, {"error": "No CSV file provided"})
                return

            reader = csv.DictReader(io.StringIO(csv_data.decode("utf-8")))
            rows = list(reader)

            if len(rows) > MAX_ROWS:
                self._json_response(400, {"error": f"Too many rows. Maximum is {MAX_ROWS}"})
                return

            results = []
            success = 0
            failed = 0
            collection = get_collection()

            for i, row in enumerate(rows, start=1):
                file_url = row.get("file_url", "").strip()
                name = row.get("name", "").strip()
                class_type = row.get("class_type", "").strip()
                user_id = row.get("user_id", "").strip()
                category = row.get("category", "").strip()
                tags_raw = row.get("tags", "").strip()

                if not file_url or not name or not class_type:
                    results.append({"row": i, "status": "error", "error": "Missing required fields (file_url, name, class_type)"})
                    failed += 1
                    continue

                if class_type not in ("avatar", "banner"):
                    results.append({"row": i, "status": "error", "error": f"Invalid class_type: {class_type}"})
                    failed += 1
                    continue

                try:
                    tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []

                    doc = create_document(
                        name=name,
                        class_type=class_type,
                        url=file_url,
                        key="",
                        file_size=0,
                        mime_type="image/jpeg",
                        user_id=user_id,
                        category=category,
                        tags=tags,
                    )

                    insert_result = collection.insert_one(doc)
                    doc["_id"] = insert_result.inserted_id

                    results.append({"row": i, "status": "ok", "url": file_url})
                    success += 1

                except Exception as e:
                    results.append({"row": i, "status": "error", "error": str(e)[:100]})
                    failed += 1

            self._json_response(200, {
                "total": len(rows),
                "success": success,
                "failed": failed,
                "results": results,
            })

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
        self.end_headers()

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

            for line in headers_raw.split("\r\n"):
                if "Content-Disposition:" in line:
                    for segment in line.split(";"):
                        segment = segment.strip()
                        if segment.startswith("name="):
                            name = segment.split("=")[1].strip('"')
                        elif segment.startswith("filename="):
                            filename = segment.split("=")[1].strip('"')

            if name:
                parts[name] = {"data": data, "filename": filename}

        return parts
