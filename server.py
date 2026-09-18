#!/usr/bin/env python3
"""Minimal worker-client HTTP server built on the Python standard library.

Endpoints:
  GET /ping      health check for this service
  GET /call-pm   proxies the puppet-master's /api/ping and returns its JSON
"""

import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE = "test-wc"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))
PM_URL = os.environ.get("PM_URL", "http://127.0.0.1:8001")
PM_TIMEOUT = float(os.environ.get("PM_TIMEOUT", "5"))


def fetch_pm_ping():
    """Return (status, payload) from the puppet-master's /api/ping."""
    url = PM_URL.rstrip("/") + "/api/ping"
    try:
        with urllib.request.urlopen(url, timeout=PM_TIMEOUT) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        return 502, {"service": SERVICE, "status": "error", "error": str(exc.reason)}
    except OSError as exc:
        return 502, {"service": SERVICE, "status": "error", "error": str(exc)}

    try:
        return 200, json.loads(body)
    except json.JSONDecodeError:
        return 502, {
            "service": SERVICE,
            "status": "error",
            "error": "puppet-master returned a non-JSON response",
        }


class Handler(BaseHTTPRequestHandler):
    server_version = "test-wc/1.0"

    def do_GET(self):
        if self.path == "/ping":
            self.respond(200, {"service": SERVICE, "status": "ok"})
        elif self.path == "/call-pm":
            self.respond(*fetch_pm_ping())
        else:
            self.respond(404, {"service": SERVICE, "status": "not_found"})

    def respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"{SERVICE} listening on http://{HOST}:{PORT} (puppet-master: {PM_URL})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
