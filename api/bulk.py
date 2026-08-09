import os
from http.server import BaseHTTPRequestHandler

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        html_path = os.path.join(STATIC_DIR, "bulk.html")
        with open(html_path, "rb") as f:
            html = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html)

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
