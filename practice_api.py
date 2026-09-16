"""Offline HTTP practice service; each exercise gets its own instance."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

requests = []

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        requests.append(self.path)
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        status = 200
        if parsed.path == '/status':
            data = {'ok': True}
        elif parsed.path == '/search':
            data = {'query': query.get('q', [''])[0]}
        elif parsed.path == '/orders':
            page = query.get('page', ['1'])[0]
            data = {'items': [{'id': 1, 'amount': 10}, {'id': 2, 'amount': 20}], 'next': '/orders?page=2'} if page == '1' else {'items': [{'id': 3, 'amount': 5}], 'next': None}
        elif parsed.path == '/unstable':
            status = 503 if requests.count('/unstable') == 1 else 200
            data = {'ok': status == 200}
        else:
            status, data = 404, {'error': 'not found'}
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
base_url = f'http://127.0.0.1:{server.server_port}'
threading.Thread(target=server.serve_forever, daemon=True).start()
