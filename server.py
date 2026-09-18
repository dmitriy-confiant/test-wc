#!/usr/bin/env python3
"""Minimal worker-client HTTP server built on the Python standard library.

Endpoints:
  GET /ping      health check for this service
  GET /call-pm   proxies the puppet-master's /api/ping and returns its JSON
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SERVICE = "test-wc"


def env_number(name, default, parse, description):
    """Read an environment variable as a number, or exit with a clear message."""
    raw = os.environ.get(name, default)
    try:
        return parse(raw)
    except ValueError:
        raise SystemExit(f"{SERVICE}: {name} must be {description}, got {raw!r}")


def env_base_url(name, default):
    """Read a base URL from the environment, rejecting non-http(s) schemes."""
    raw = os.environ.get(name, default)
    if urllib.parse.urlsplit(raw).scheme not in ("http", "https"):
        raise SystemExit(f"{SERVICE}: {name} must be an http:// or https:// URL, got {raw!r}")
    return raw


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = env_number("PORT", "8000", int, "an integer")
PM_BASE_URL = env_base_url("PM_BASE_URL", "http://localhost:3000")
PM_TIMEOUT = env_number("PM_TIMEOUT", "5", float, "a number of seconds")


def fetch_pm_ping():
    """Return (status, payload) from the puppet-master's /api/ping."""
    url = PM_BASE_URL.rstrip("/") + "/api/ping"
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
        path = self.path.split("?", 1)[0].rstrip("/") or "/"
        if path == "/ping":
            self.respond(200, {"service": SERVICE, "status": "ok"})
        elif path == "/call-pm":
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
    print(f"{SERVICE} listening on http://{HOST}:{PORT} (puppet-master: {PM_BASE_URL})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
