import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
from bson import ObjectId

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.mongodb import get_collection
from lib.uploadthing import UploadThingClient
from lib.models import to_response


class handler(BaseHTTPRequestHandler):
    def _json_response(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_params(self):
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)

    def do_GET(self):
        params = self._get_params()
        image_id = params.get("id", [None])[0]
        user_id = params.get("user_id", [None])[0]
        class_type = params.get("class_type", [None])[0]
        category = params.get("category", [None])[0]
        tags = params.get("tags", [None])[0]

        try:
            collection = get_collection()

            if image_id:
                doc = collection.find_one({"_id": ObjectId(image_id)})
                if not doc:
                    self._json_response(404, {"error": "Image not found"})
                    return
                self._json_response(200, to_response(doc))
                return

            if not user_id:
                self._json_response(400, {"error": "user_id is required"})
                return

            query = {"user_id": user_id}
            if class_type:
                query["class_type"] = class_type
            if category:
                query["category"] = category
            if tags:
                tag_list = [t.strip() for t in tags.split(",") if t.strip()]
                if tag_list:
                    query["tags"] = {"$all": tag_list}

            docs = list(collection.find(query).sort("created_at", -1))
            results = [to_response(doc) for doc in docs]
            self._json_response(200, results)

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_PUT(self):
        params = self._get_params()
        image_id = params.get("id", [None])[0]

        if not image_id:
            self._json_response(400, {"error": "id parameter is required"})
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
        params = self._get_params()
        image_id = params.get("id", [None])[0]

        if not image_id:
            self._json_response(400, {"error": "id parameter is required"})
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
