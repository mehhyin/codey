"""A zero-service, loopback-only Python learning app."""
import argparse
import json
import os
import secrets
import subprocess
import sys
import shutil
import uuid
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from course import all_tasks, public_course

ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
SLOTS = threading.BoundedSemaphore(2)
TIMEOUT = 8
CREATE_FLAGS = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
RUN_ROOT = ROOT.parent.parent / 'work' / 'pyroom-runs'


def execute(task, code, mode):
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    path = RUN_ROOT / uuid.uuid4().hex
    path.mkdir()
    try:
        for name, content in task['files'].items():
            target = path / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        (path / 'main.py').write_text(code, encoding='utf-8')
        (path / 'request.json').write_text(json.dumps(dict(code=code, mode=mode, checks=task['checks'])), encoding='utf-8')
        try:
            completed = subprocess.run([sys.executable, '-I', str(ROOT / 'worker.py')], cwd=path,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=TIMEOUT, creationflags=CREATE_FLAGS)
        except subprocess.TimeoutExpired:
            return dict(output='', error='Time limit reached. Check for an endless loop or a program waiting for input. Each run has 8 seconds.', checks=[], passed=False)
        result_file = path / 'result.json'
        if completed.returncode != 0 or not result_file.exists():
            return dict(output='', error='Python stopped before finishing. Remove exit calls and try again.', checks=[], passed=False)
        return json.loads(result_file.read_text(encoding='utf-8'))
    finally:
        # Delete only this attempt's verified descendant of the practice-run root.
        if path.resolve().parent == RUN_ROOT.resolve() and not path.is_symlink():
            shutil.rmtree(path, ignore_errors=True)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, data, mime='application/json', status=200):
        if not isinstance(data, bytes):
            data = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def valid_host(self):
        return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}')

    def do_GET(self):
        if not self.valid_host():
            return self.send({'error': 'Local access only.'}, status=403)
        route = urlsplit(self.path).path
        if route == '/api/health':
            return self.send({'app': 'pyroom', 'version': 1})
        if route == '/api/course':
            return self.send({'modules': public_course(), 'token': TOKEN})
        assets = {'/': ('index.html', 'text/html; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
                  '/style.css': ('style.css', 'text/css; charset=utf-8'), '/favicon.svg': ('favicon.svg', 'image/svg+xml')}
        if route not in assets:
            return self.send({'error': 'Not found'}, status=404)
        name, mime = assets[route]
        return self.send((ROOT / 'dist' / name).read_bytes(), mime)

    def do_POST(self):
        origin = self.headers.get('Origin')
        expected = f'http://{self.headers.get("Host")}'
        if not self.valid_host() or (origin is not None and origin != expected) or self.headers.get('X-Pyroom-Token') != TOKEN:
            return self.send({'error': 'Please refresh Pyroom and try again.'}, status=403)
        if self.headers.get('Content-Type') != 'application/json':
            return self.send({'error': 'Expected JSON.'}, status=415)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 100000:
                return self.send({'error': 'Request is too large.'}, status=413)
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError()
            if self.path == '/api/shutdown':
                self.send({'stopped': True})
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return
            task_id = data.get('task')
            if not isinstance(task_id, str):
                raise ValueError()
            task = all_tasks().get(task_id)
            if task is None:
                return self.send({'error': 'Lesson not found.'}, status=404)
        except (ValueError, TypeError):
            return self.send({'error': 'Invalid request.'}, status=400)
        if self.path == '/api/solution':
            return self.send({'solution': task['solution'], 'explanation': task['explanation']})
        if self.path != '/api/execute':
            return self.send({'error': 'Not found.'}, status=404)
        code, mode = data.get('code'), data.get('mode')
        if not isinstance(code, str) or len(code) > 50000 or mode not in ('run', 'submit'):
            return self.send({'error': 'Invalid code or action.'}, status=400)
        if not SLOTS.acquire(blocking=False):
            return self.send({'error': 'Two attempts are already running. Try again shortly.'}, status=429)
        try:
            result = execute(task, code, mode)
            if result.get('passed'):
                result['explanation'] = task['explanation']
            return self.send(result)
        except Exception:
            return self.send({'error': 'This attempt could not finish. Try again or restart Pyroom.'}, status=500)
        finally:
            SLOTS.release()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--open', action='store_true')
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    except OSError as exc:
        print(f'Cannot start Pyroom on port {args.port}: {exc}', flush=True)
        return 1
    print(f'Pyroom is ready at http://127.0.0.1:{args.port}', flush=True)
    if args.open:
        webbrowser.open(f'http://127.0.0.1:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
