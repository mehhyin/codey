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
import base64
import time
import atexit
import ast
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
PREVIEW_LOCK = threading.RLock()
PREVIEW = None


def prepare(task, code, directory, extra=None, mode='run'):
    for name, content in task['files'].items():
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
    for name, content in (extra or {}).items():
        if name not in task.get('editor_files', {}) or name == 'main.py':
            raise ValueError('Unknown project file')
        (directory / name).write_text(content, encoding='utf-8')
    for name, content in task.get('editor_files', {}).items():
        if name != 'main.py' and name not in (extra or {}):
            (directory / name).write_text('', encoding='utf-8')
    (directory / 'main.py').write_text(code, encoding='utf-8')
    # Grading dependencies belong to the checks, never to learner globals.
    referenced = {node.id for check in task['checks'] for node in ast.walk(ast.parse(check['code']))
                  if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
    check_imports = []
    for node in ast.parse(task['starter']).body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = {alias.asname or alias.name.split('.')[0] for alias in node.names}
            if names & referenced:
                check_imports.append(ast.unparse(node))
    (directory / 'request.json').write_text(json.dumps(dict(code=code, mode=mode,
        setup=task.get('setup', ''), check_imports='\n'.join(check_imports), checks=task['checks'])), encoding='utf-8')


def stop_preview():
    global PREVIEW
    with PREVIEW_LOCK:
        if PREVIEW:
            process, directory = PREVIEW
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=3)
            if directory.resolve().parent == RUN_ROOT.resolve() and not directory.is_symlink():
                shutil.rmtree(directory, ignore_errors=True)
            PREVIEW = None


atexit.register(stop_preview)


def launch_preview(task, code, extra=None):
    global PREVIEW
    with PREVIEW_LOCK:
        stop_preview()
        RUN_ROOT.mkdir(parents=True, exist_ok=True)
        directory = RUN_ROOT / uuid.uuid4().hex
        directory.mkdir()
        prepare(task, code, directory, extra)
        secret = secrets.token_urlsafe(24)
        with (directory / 'preview-error.log').open('w', encoding='utf-8') as error_log:
            process = subprocess.Popen([sys.executable, '-I', str(ROOT / 'project_preview.py'), secret],
                cwd=directory, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=error_log,
                creationflags=CREATE_FLAGS)
        PREVIEW = process, directory
        for _ in range(100):
            ready = directory / 'ready.json'
            if ready.exists():
                try:
                    result = json.loads(ready.read_text(encoding='utf-8'))
                    result['url'] += task.get('preview_path', '')
                    return result
                except json.JSONDecodeError:
                    pass
            if process.poll() is not None:
                stop_preview()
                raise ValueError('Preview could not start. Check that your code defines app and runs without errors.')
            time.sleep(0.1)
        stop_preview()
        raise ValueError('Preview startup timed out. Remove app.run() and long-running code, then try again.')


def execute(task, code, mode, extra=None):
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    path = RUN_ROOT / uuid.uuid4().hex
    path.mkdir()
    try:
        prepare(task, code, path, extra, mode)
        limit = task.get('time_limit', TIMEOUT)
        try:
            completed = subprocess.run([sys.executable, '-I', str(ROOT / 'worker.py')], cwd=path,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                timeout=limit, creationflags=CREATE_FLAGS)
        except subprocess.TimeoutExpired:
            return dict(output='', error=f'Time limit reached. Check for an endless loop or a program waiting for input. This run has {limit} seconds.', checks=[], passed=False)
        result_file = path / 'result.json'
        if completed.returncode != 0 or not result_file.exists():
            return dict(output='', error='Python stopped before finishing. Remove exit calls and try again.', checks=[], passed=False)
        result = json.loads(result_file.read_text(encoding='utf-8'))
        result['artifacts'] = []
        allowed = list(dict.fromkeys(result.pop('plots', []) + task.get('exports', [])))
        total_bytes = 0
        for name in allowed[:8]:
            target = path / name
            if not target.is_file() or target.is_symlink() or target.resolve().parent != path.resolve():
                continue
            size = target.stat().st_size
            if size > 2_000_000 or total_bytes + size > 6_000_000:
                continue
            total_bytes += size
            mime = {'.png':'image/png', '.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                '.csv':'text/csv', '.html':'text/html', '.json':'application/json', '.txt':'text/plain'}.get(target.suffix)
            if mime:
                result['artifacts'].append({'name': name, 'mime': mime, 'data': base64.b64encode(target.read_bytes()).decode('ascii')})
        return result
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
            return self.send({'app': 'pyroom', 'version': 2})
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
            return self.send({'solution': task['solution'], 'files': task.get('solution_files', {}), 'explanation': task['explanation']})
        if self.path not in ('/api/execute', '/api/preview'):
            return self.send({'error': 'Not found.'}, status=404)
        code, mode = data.get('code'), data.get('mode')
        extra = data.get('files', {})
        if not isinstance(extra, dict) or any(not isinstance(name, str) or name not in task.get('editor_files', {})
                or name == 'main.py' or not isinstance(value, str) or len(value) > 50000 for name, value in extra.items()):
            return self.send({'error': 'Invalid project files.'}, status=400)
        if not isinstance(code, str) or len(code) > 50000 or mode not in ('run', 'submit'):
            return self.send({'error': 'Invalid code or action.'}, status=400)
        if not SLOTS.acquire(blocking=False):
            return self.send({'error': 'Two attempts are already running. Try again shortly.'}, status=429)
        try:
            if self.path == '/api/preview':
                if not task.get('web_preview'):
                    return self.send({'error': 'This lesson does not have a web preview.'}, status=400)
                try:
                    return self.send(launch_preview(task, code, extra))
                except ValueError as exc:
                    return self.send({'error': str(exc)}, status=400)
            result = execute(task, code, mode, extra)
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
        stop_preview()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
