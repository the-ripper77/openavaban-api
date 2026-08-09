import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.uploadthing import UploadThingClient
from lib.mongodb import get_collection
from lib.models import create_document, to_response


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers.get("Content-Type", "")

        if "multipart/form-data" not in content_type:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Content-Type must be multipart/form-data"}).encode())
            return

        boundary = content_type.split("boundary=")[1]
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        parts = self._parse_multipart(body, boundary)

        file_data = parts.get("file", {}).get("data")
        file_name = parts.get("file", {}).get("filename", "unknown")
        file_type = parts.get("file", {}).get("content_type", "application/octet-stream")

        if not file_data:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No file provided"}).encode())
            return

        name = parts.get("name", {}).get("data", b"").decode()
        class_type = parts.get("class_type", {}).get("data", b"").decode()
        user_id = parts.get("user_id", {}).get("data", b"").decode()
        category = parts.get("category", {}).get("data", b"").decode()
        tags_raw = parts.get("tags", {}).get("data", b"").decode()
        metadata_raw = parts.get("metadata", {}).get("data", b"").decode()

        tags = [t.strip() for t in tags_raw.split(",") if t.strip()] if tags_raw else []
        metadata = json.loads(metadata_raw) if metadata_raw else {}

        if not name or not class_type:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "name and class_type are required"}).encode())
            return

        try:
            uploadthing = UploadThingClient()
            result = uploadthing.upload(file_data, file_name, file_type)

            dimensions = None
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(file_data))
                dimensions = {"width": img.width, "height": img.height}
            except Exception:
                pass

            doc = create_document(
                name=name,
                class_type=class_type,
                url=result["url"],
                key=result["key"],
                file_size=result["size"],
                mime_type=result["type"],
                user_id=user_id,
                category=category,
                tags=tags,
                metadata=metadata,
                dimensions=dimensions,
            )

            collection = get_collection()
            insert_result = collection.insert_one(doc)
            doc["_id"] = insert_result.inserted_id

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(to_response(doc)).encode())

        except ValueError as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _parse_multipart(self, body: bytes, boundary: str) -> dict:
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
