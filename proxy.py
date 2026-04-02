# v1.3.0
"""
Senior Agent Debug — Proxy local
Serve o HTML, repassa chamadas ao MLflow, Gemini e Wiki Senior.

Uso:
    pip install flask requests
    GEMINI_API_KEY=AIza... python proxy.py
    Abrir: http://127.0.0.1:5000
"""

import os, json
import requests
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__)

MLFLOW_BASE    = "http://agentx-homolog-mlflow-alb-1239989404.us-east-1.elb.amazonaws.com"
GEMINI_API_KEY   = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL     = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_BASE_URL  = "https://generativelanguage.googleapis.com/v1/models"
HTML_FILE        = os.path.join(os.path.dirname(__file__), "senior-agent-debug.html")

def cors(h):
    h["Access-Control-Allow-Origin"]  = "*"
    h["Access-Control-Allow-Headers"] = "*"
    h["Access-Control-Allow-Methods"] = "*"
    return h

EXCLUDED = {"host","content-length","transfer-encoding","connection",
            "keep-alive","proxy-authenticate","proxy-authorization",
            "te","trailers","upgrade","content-encoding"}

def fwd_headers(headers):
    return {k: v for k, v in headers if k.lower() not in EXCLUDED}

# ── HTML ───────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(HTML_FILE), "senior-agent-debug.html")

# ── MLflow proxy ───────────────────────────────────────────────────────────────
@app.route("/mlflow/<path:path>", methods=["GET","POST","PUT","DELETE","OPTIONS"])
def mlflow_proxy(path):
    url = f"{MLFLOW_BASE}/ajax-api/{path}"
    qs  = request.query_string.decode("utf-8")
    if qs:
        url = f"{url}?{qs}"
    try:
        resp = requests.request(
            method=request.method, url=url,
            headers=fwd_headers(request.headers),
            data=request.get_data(), timeout=30, allow_redirects=True,
        )
    except requests.exceptions.RequestException as e:
        return Response(f'{{"error":"{e}"}}', status=502, mimetype="application/json")
    h = cors({k: v for k, v in resp.headers.items() if k.lower() not in EXCLUDED})
    return Response(resp.content, status=resp.status_code, headers=h)

# ── Wiki: carregada diretamente pelo browser com credentials:'include' (SSO Windows)
# Não passa pelo proxy — o browser envia Kerberos/NTLM automaticamente.

# ── Gemini proxy ───────────────────────────────────────────────────────────────
@app.route("/gemini", methods=["POST","OPTIONS"])
def gemini_proxy():
    if request.method == "OPTIONS":
        return Response("", status=204, headers=cors({}))
    if not GEMINI_API_KEY:
        msg = '{"error":"GEMINI_API_KEY nao configurada. Inicie com: GEMINI_API_KEY=AIza... python proxy.py"}'
        return Response(msg, status=500, headers=cors({"Content-Type":"application/json"}))
    try:
        body = request.get_json(force=True)
        # Allow frontend to specify model, fallback to env/default
        model = (body or {}).pop("_model", GEMINI_MODEL)
        url = f"{GEMINI_BASE_URL}/{model}:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json=body, timeout=120)
        h = cors({"Content-Type": "application/json"})
        return Response(resp.content, status=resp.status_code, headers=h)
    except requests.exceptions.RequestException as e:
        return Response(f'{{"error":"{e}"}}', status=502, headers=cors({"Content-Type":"application/json"}))

if __name__ == "__main__":
    key_ok = bool(GEMINI_API_KEY)
    print("=" * 62)
    print("  Senior Agent Debug  —  http://127.0.0.1:5000  [proxy v1.3.0]")
    print(f"  Gemini API Key : {'OK configurada' if key_ok else 'NAO configurada'}")
    print(f"  Gemini Model   : {GEMINI_MODEL}")
    if not key_ok:
        print("  -> export GEMINI_API_KEY=AIza...  (ou set no Windows)")
    print("=" * 62)
    app.run(host="127.0.0.1", port=5000, debug=False)
