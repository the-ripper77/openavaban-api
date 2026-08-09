import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from bson import ObjectId

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from middleware import check_api_key
from lib.mongodb import get_collection
from lib.uploadthing import UploadThingClient
from lib.models import to_response


class handler(BaseHTTPRequestHandler):
    def _get_id_from_path(self):
        path = self.path.rstrip("/")
        parts = path.split("/")
        return parts[-1] if parts else None

    def do_GET(self):
        auth_ok, auth_err = check_api_key(self)
        if not auth_ok:
            self._json_response(401, {"error": auth_err})
            return

        image_id = self._get_id_from_path()
        if not image_id:
            self._json_response(400, {"error": "Missing image ID"})
            return

        try:
            collection = get_collection()
            doc = collection.find_one({"_id": ObjectId(image_id)})
            if not doc:
                self._json_response(404, {"error": "Image not found"})
                return

            self._json_response(200, to_response(doc))
        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_PUT(self):
        auth_ok, auth_err = check_api_key(self)
        if not auth_ok:
            self._json_response(401, {"error": auth_err})
            return

        image_id = self._get_id_from_path()
        if not image_id:
            self._json_response(400, {"error": "Missing image ID"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._json_response(400, {"error": "Invalid JSON"})
            return

        allowed_fields = {"name", "category", "tags", "metadata", "class_type"}
        updates = {k: v for k, v in data.items() if k in allowed_fields}

        if not updates:
            self._json_response(400, {"error": "No valid fields to update"})
            return

        if "class_type" in updates and updates["class_type"] not in ("avatar", "banner"):
            self._json_response(400, {"error": "class_type must be 'avatar' or 'banner'"})
            return

        from datetime import datetime, timezone
        updates["updated_at"] = datetime.now(timezone.utc)

        try:
            collection = get_collection()
            result = collection.update_one(
                {"_id": ObjectId(image_id)},
                {"$set": updates},
            )

            if result.matched_count == 0:
                self._json_response(404, {"error": "Image not found"})
                return

            doc = collection.find_one({"_id": ObjectId(image_id)})
            self._json_response(200, to_response(doc))

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_DELETE(self):
        auth_ok, auth_err = check_api_key(self)
        if not auth_ok:
            self._json_response(401, {"error": auth_err})
            return

        image_id = self._get_id_from_path()
        if not image_id:
            self._json_response(400, {"error": "Missing image ID"})
            return

        try:
            collection = get_collection()
            doc = collection.find_one({"_id": ObjectId(image_id)})

            if not doc:
                self._json_response(404, {"error": "Image not found"})
                return

            uploadthing = UploadThingClient()
            uploadthing.delete(doc["key"])

            collection.delete_one({"_id": ObjectId(image_id)})

            self._json_response(200, {"success": True, "deleted": image_id})

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def _json_response(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
