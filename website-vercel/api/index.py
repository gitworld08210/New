import json
import os
import random
import re
import urllib.request
from http.server import BaseHTTPRequestHandler

SUPABASE_URL = os.environ.get(
    "SUPABASE_URL", "https://ijkxadnmeqfflfuwvmfz.supabase.co"
)
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
MODEL_API_URL = os.environ.get("MODEL_API_URL", "").rstrip("/")
MODEL_API_TOKEN = os.environ.get("MODEL_API_TOKEN", "")

SHORT_KEYWORDS = {
    "hi", "hey", "ok", "no", "ha", "na", "kya", "ho", "so", "tu",
    "hii", "bye", "gm", "gn",
}
DEFAULTS = [
    "Hmm batao? 😊", "Accha! Phir? 🤔", "Nice! 😄", "Sahi hai! 😊",
    "Aur bata? 🤗", "Interesting! 😄", "Mast! 🙌",
]


def model_reply(message):
    """Use a separately hosted trained Flask model when configured."""
    if not MODEL_API_URL:
        return None
    try:
        headers = {"Content-Type": "application/json"}
        if MODEL_API_TOKEN:
            headers["Authorization"] = f"Bearer {MODEL_API_TOKEN}"
        payload = json.dumps({"message": message}).encode("utf-8")
        request = urllib.request.Request(
            f"{MODEL_API_URL}/api/chat",
            data=payload,
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        reply = data.get("reply")
        return reply.strip() if isinstance(reply, str) and reply.strip() else None
    except Exception:
        return None


def load_responses():
    if not SUPABASE_KEY:
        return {}
    try:
        url = (
            f"{SUPABASE_URL}/rest/v1/bot_responses"
            "?select=keyword,response&limit=2000"
        )
        request = urllib.request.Request(
            url,
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        responses = {}
        for item in data:
            keyword = item.get("keyword")
            reply = item.get("response")
            if not isinstance(keyword, str) or not isinstance(reply, str):
                continue
            keyword = keyword.lower().strip()
            if keyword:
                responses.setdefault(keyword, []).append(reply)
        return responses
    except Exception:
        return {}


def get_reply(message, responses):
    text = message.lower().strip()
    for keyword, replies in responses.items():
        if text == keyword:
            return random.choice(replies)

    for keyword in sorted(responses, key=len, reverse=True):
        if len(keyword) <= 3 or keyword in SHORT_KEYWORDS:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                return random.choice(responses[keyword])
        elif keyword in text:
            return random.choice(responses[keyword])
    return random.choice(DEFAULTS)


class handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16_384:
                return self._json(400, {"error": "Invalid request body"})
            data = json.loads(self.rfile.read(length))
            message = data.get("message", "")
            if not isinstance(message, str) or not message.strip():
                return self._json(400, {"error": "Message is required"})
            message = message.strip()
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Invalid JSON"})

        reply = model_reply(message)
        if not reply:
            reply = get_reply(message, load_responses())
        return self._json(200, {"reply": reply})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
