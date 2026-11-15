"""Temporary: serve a demo page that renders /api/v1/analyze output in a browser.

Renders the response the way Member 1 is told to in docs/contracts.md:
warning as the headline, recommended_actions as a list, colour by overall_risk.
"""

import json
import subprocess
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Elderly Safety Companion - Risk Report</title>
<style>
  :root { --low:#177245; --medium:#a15c00; --high:#b3261e; --degraded:#5f6368; }
  body { font-family: Segoe UI, Arial, sans-serif; background:#f6f4ef; margin:0; padding:40px; }
  .card { max-width:760px; margin:0 auto; background:#fff; border-radius:16px;
          box-shadow:0 2px 14px rgba(0,0,0,.10); overflow:hidden; }
  .banner { padding:28px 32px; color:#fff; }
  .banner .level { font-size:15px; letter-spacing:.14em; text-transform:uppercase; opacity:.92; }
  .banner h1 { font-size:28px; line-height:1.35; margin:10px 0 0; font-weight:600; }
  .body { padding:26px 32px 34px; }
  .badge { display:inline-block; font-size:13px; padding:3px 10px; border-radius:999px;
           background:#eceff1; color:#37474f; margin-bottom:18px; }
  h2 { font-size:17px; color:#263238; margin:26px 0 10px; }
  ul { margin:0; padding-left:22px; }
  li { font-size:17px; line-height:1.7; color:#1f2a30; margin-bottom:8px; }
  .meta { font-size:13px; color:#607d8b; margin-top:24px; }
  .meta code { background:#eceff1; padding:1px 6px; border-radius:4px; }
</style>
</head>
<body>
  <div class="card">
    <div class="banner" id="banner">
      <div class="level" id="level">Loading...</div>
      <h1 id="warning">Fetching risk assessment...</h1>
    </div>
    <div class="body">
      <span class="badge" id="status">status: unknown</span>
      <h2>What we noticed</h2>
      <ul id="indicators"><li>...</li></ul>
      <h2>What you should do</h2>
      <ul id="actions"><li>...</li></ul>
      <p class="meta" id="meta"></p>
    </div>
  </div>
<script>
const COLOURS = { LOW:"var(--low)", MEDIUM:"var(--medium)", HIGH:"var(--high)" };
async function run() {
  const res = await fetch("http://127.0.0.1:8000/api/v1/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: "See http://paypa1-login.com/verify for details." })
  });
  const data = await res.json();
  window.__result = data;

  document.getElementById("banner").style.background =
      COLOURS[data.overall_risk] || "var(--degraded)";
  document.getElementById("level").textContent = data.overall_risk + " RISK";
  document.getElementById("warning").textContent = data.warning;
  document.getElementById("status").textContent =
      "status: " + data.status + "   |   message: " + data.message_prediction +
      "   |   link: " + data.url_risk;

  document.getElementById("indicators").innerHTML =
      (data.risk_indicators.length ? data.risk_indicators : ["Nothing specific was flagged."])
        .map(t => "<li>" + t + "</li>").join("");
  document.getElementById("actions").innerHTML =
      data.recommended_actions.map(t => "<li>" + t + "</li>").join("");
  document.getElementById("meta").innerHTML =
      "Score " + data.score.total + " / thresholds " + JSON.stringify(data.score.thresholds) +
      "<br>Modules: " + data.module_status.map(m => m.name + "=" + m.state).join(", ") +
      "<br>Rule set v" + data.config_version + " &#183; " + data.analysis_id;
}
run().catch(e => { document.getElementById("warning").textContent = "ERROR: " + e; });
</script>
</body>
</html>
"""


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    import scratch_stub_modules as stubs

    stubs.serve(stubs.ScamHandler, 8001)
    stubs.serve(stubs.MaliciousUrl, 8002)
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000",
         "--log-level", "warning"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        try:
            urllib.request.urlopen("http://127.0.0.1:8000/api/v1/health", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    srv = ThreadingHTTPServer(("127.0.0.1", 8010), Page)
    print("page ready at http://127.0.0.1:8010/", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait(timeout=10)
