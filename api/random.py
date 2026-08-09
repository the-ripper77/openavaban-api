import json
import os
import sys
import random as rnd
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

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        category = params.get("category", [None])[0]
        count = min(int(params.get("count", [1])[0]), 25)

        try:
            collection = get_collection()
            query = {}
            if category:
                query["category"] = {"$regex": category, "$options": "i"}

            total = collection.count_documents(query)
            if total == 0:
                self._json_response(200, [] if count > 1 else {"error": "No images found"})
                return

            if count >= total:
                docs = list(collection.find(query))
            else:
                pipeline = [{"$match": query}, {"$sample": {"size": count}}]
                docs = list(collection.aggregate(pipeline))

            results = [to_response(doc) for doc in docs]

            if count == 1:
                self._json_response(200, results[0])
            else:
                self._json_response(200, results)

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
