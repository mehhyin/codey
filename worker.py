"""Execute one learner attempt in a disposable working directory (not a security sandbox)."""
import contextlib
import io
import json
import sys
import traceback
from pathlib import Path


class BoundedOutput(io.StringIO):
    def write(self, text):
        room = max(0, 24000 - self.tell())
        super().write(text[:room])
        return len(text)


def main():
    payload = json.loads(Path('request.json').read_text(encoding='utf-8'))
    output, errors = BoundedOutput(), BoundedOutput()
    namespace = {'__name__': '__main__', '__file__': str(Path('main.py').resolve())}
    result = {'output': '', 'error': None, 'checks': [], 'passed': False}
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            exec(compile(payload['code'], 'main.py', 'exec'), namespace)
    except BaseException as exc:
        if isinstance(exc, SyntaxError):
            result['error'] = f'{type(exc).__name__} on line {exc.lineno}: {exc.msg}'
        else:
            frames = traceback.extract_tb(exc.__traceback__)
            learner = [f for f in frames if f.filename == 'main.py']
            location = f' on line {learner[-1].lineno}' if learner else ''
            result['error'] = f'{type(exc).__name__}{location}: {str(exc)[:1000]}'
    result['output'] = output.getvalue()
    if output.tell() >= 24000:
        result['output'] += '\n[Output truncated at 24,000 characters.]'
    result['stderr'] = errors.getvalue()
    if not result['error'] and payload['mode'] == 'submit':
        namespace['__output__'] = result['output']
        for check in payload['checks']:
            try:
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    exec(check['code'], namespace)
                result['checks'].append({'label': check['label'], 'passed': True})
            except BaseException:
                result['checks'].append({'label': check['label'], 'passed': False})
        result['passed'] = bool(result['checks']) and all(c['passed'] for c in result['checks'])
    Path('result.json').write_text(json.dumps(result), encoding='utf-8')


if __name__ == '__main__':
    main()
