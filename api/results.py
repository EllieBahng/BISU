import os, json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
RESULTS_PASSWORD = os.environ.get('RESULTS_PASSWORD', 'teacher123')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        pw = params.get('pw', [''])[0]

        if pw != RESULTS_PASSWORD:
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'unauthorized'}).encode())
            return

        try:
            url = f"{SUPABASE_URL}/rest/v1/responses?select=*&order=created_at.desc"
            req = urllib.request.Request(url, headers={
                'apikey': SUPABASE_SERVICE_KEY,
                'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                'Content-Type': 'application/json'
            })
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def log_message(self, format, *args):
        pass
