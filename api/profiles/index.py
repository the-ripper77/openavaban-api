import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from middleware import check_api_key
from lib.mongodb import get_collection
from lib.models import to_response


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_ok, auth_err = check_api_key(self)
        if not auth_ok:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": auth_err}).encode())
            return

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        user_id = params.get("user_id", [None])[0]
        class_type = params.get("class_type", [None])[0]
        category = params.get("category", [None])[0]
        tags = params.get("tags", [None])[0]

        if not user_id:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "user_id is required"}).encode())
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

        try:
            collection = get_collection()
            docs = list(collection.find(query).sort("created_at", -1))
            results = [to_response(doc) for doc in docs]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
