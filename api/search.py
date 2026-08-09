import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.mongodb import get_collection
from lib.models import to_response


class handler(BaseHTTPRequestHandler):
    def _json_response(self, status: int, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_params(self):
        parsed = urlparse(self.path)
        return parse_qs(parsed.query)

    def do_GET(self):
        params = self._get_params()

        query_text = params.get("q", [None])[0]
        class_type = params.get("class_type", [None])[0]
        category = params.get("category", [None])[0]
        tags = params.get("tags", [None])[0]
        mime_type = params.get("mime_type", [None])[0]
        limit = min(int(params.get("limit", [30])[0]), 100)
        offset = int(params.get("offset", [0])[0])

        try:
            collection = get_collection()
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
            docs = list(
                collection.find(query)
                .sort("created_at", -1)
                .skip(offset)
                .limit(limit)
            )
            results = [to_response(doc) for doc in docs]

            self._json_response(
                200,
                {
                    "total": total,
                    "offset": offset,
                    "limit": limit,
                    "has_more": (offset + limit) < total,
                    "results": results,
                },
            )

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
