"""Run a learner's Flask project on loopback, beneath an unguessable mount path."""
import json
from pathlib import Path
import runpy
import sys
import time
import threading
from wsgiref.simple_server import make_server, WSGIRequestHandler
sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_runtime import configure

configure()


class QuietHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass


def main():
    secret = sys.argv[1]
    payload = json.loads(Path('request.json').read_text(encoding='utf-8'))
    exec(payload.get('setup', ''), {'__name__': '__fixture__'})
    namespace = runpy.run_path('main.py', run_name='learner_preview')
    app = namespace.get('app')
    if not callable(app):
        raise ValueError('Define a Flask application named app before opening a preview.')
    prefix = '/' + secret

    def mounted(environ, start_response):
        host = f'127.0.0.1:{httpd.server_port}'
        path = environ.get('PATH_INFO', '')
        origin = environ.get('HTTP_ORIGIN')
        if (environ.get('HTTP_HOST') != host or not path.startswith(prefix + '/')
                or (origin is not None and origin != 'http://' + host)):
            start_response('403 Forbidden', [('Content-Type', 'text/plain')])
            return [b'Open this project using its Pyroom preview link.']
        environ['SCRIPT_NAME'] = prefix
        environ['PATH_INFO'] = path[len(prefix):]
        return app(environ, start_response)

    httpd = make_server('127.0.0.1', 0, mounted, handler_class=QuietHandler)
    httpd.timeout = 1
    Path('ready.json').write_text(json.dumps({'url': f'http://127.0.0.1:{httpd.server_port}{prefix}/'}), encoding='utf-8')
    # Previews are temporary study sessions, not background deployments.
    deadline = time.monotonic() + 3600
    while time.monotonic() < deadline:
        httpd.handle_request()
    httpd.server_close()


if __name__ == '__main__':
    main()
