from http.server import BaseHTTPRequestHandler
import json
import random
import re
import os
import urllib.request

SUPABASE_URL = "https://ijkxadnmeqfflfuwvmfz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlqa3hhZG5tZXFmZmxmdXd2bWZ6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcyMTg0MTUsImV4cCI6MjEwMjc5NDQxNX0.i-fNXpFmLTGC635QUD33n7neNUarentevjyUxp4I4FA"

SHORT_KEYWORDS = {"hi", "hey", "ok", "no", "ha", "na", "kya", "ho", "so", "tu", "hii", "bye", "gm", "gn"}
defaults = ["Hmm batao? 😊", "Accha! Phir? 🤔", "Nice! 😄", "Sahi hai! 😊", "Aur bata? 🤗", "Interesting! 😄", "Mast! 🙌"]

# Cache responses (refresh every request for serverless)
def load_responses():
    try:
        url = f"{SUPABASE_URL}/rest/v1/bot_responses?select=keyword,response&limit=2000"
        req = urllib.request.Request(url, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            responses = {}
            for item in data:
                kw = item["keyword"].lower().strip()
                if kw not in responses:
                    responses[kw] = []
                responses[kw].append(item["response"])
            return responses
    except:
        return {}

def get_reply(msg, responses):
    m = msg.lower().strip()
    for k, v in responses.items():
        if m == k:
            return random.choice(v)
    sorted_kw = sorted(responses.keys(), key=len, reverse=True)
    for k in sorted_kw:
        if len(k) <= 3 or k in SHORT_KEYWORDS:
            pattern = r'\b' + re.escape(k) + r'\b'
            if re.search(pattern, m):
                return random.choice(responses[k])
        else:
            if k in m:
                return random.choice(responses[k])
    return random.choice(defaults)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)
        message = data.get("message", "")

        responses = load_responses()
        reply = get_reply(message, responses)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"reply": reply}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
