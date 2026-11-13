"""Temporary stand-ins for Member 2 and Member 3, used only to demo the HTTP path."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread


class ScamHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        message = json.loads(body or b"{}").get("message", "")
        low = message.lower()
        if "otp" in low or "urgent" in low:
            out = {"prediction": "SCAM", "confidence": 0.94,
                   "signals": ["otp_request", "urgency"]}
        elif "http" in low:
            out = {"prediction": "SCAM", "confidence": 0.61, "signals": ["urgency"]}
        else:
            out = {"prediction": "LEGITIMATE", "confidence": 0.08, "signals": []}
        self._send(out)

    def _send(self, out):
        payload = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


class UrlHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        url = json.loads(body or b"{}").get("url", "")
        if ".xyz" in url:
            out = {"url_risk": "SUSPICIOUS",
                   "flags": ["shortened", "no_https"], "score": 0.61}
        else:
            out = {"url_risk": "SAFE", "flags": [], "score": 0.05}
        payload = json.dumps(out).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


class MaliciousUrl(ScamHandler):
    """Reuses ScamHandler only for its _send helper."""

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        _ = json.loads(body or b"{}")
        self._send({"url_risk": "MALICIOUS", "flags": ["lookalike"], "score": 0.93})


def serve(handler, port):
    srv = ThreadingHTTPServer(("127.0.0.1", port), handler)
    Thread(target=srv.serve_forever, daemon=True).start()
    return srv
