"""Execute one learner attempt in a disposable working directory (not a security sandbox)."""
import contextlib
import io
import json
import sys
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_runtime import configure

configure()


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
            exec(payload.get('setup', ''), {'__name__': '__fixture__'})
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
    # Capture learner-created figures before checks can alter them.
    result['plots'] = []
    if 'matplotlib.pyplot' in sys.modules and not result['error']:
        try:
            plt = sys.modules['matplotlib.pyplot']
            for number in plt.get_fignums()[:4]:
                filename = f'pyroom-plot-{number}.png'
                plt.figure(number).savefig(filename, dpi=110, bbox_inches='tight')
                result['plots'].append(filename)
        except Exception as exc:
            result['error'] = f'Chart rendering failed: {str(exc)[:1000]}'
    if not result['error'] and payload['mode'] == 'submit':
        check_namespace = dict(namespace, __output__=result['output'], __learner_globals__=namespace)
        for check in payload['checks']:
            try:
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                    exec(payload.get('check_imports', '') + '\n' + check['code'], check_namespace)
                result['checks'].append({'label': check['label'], 'passed': True})
            except BaseException:
                result['checks'].append({'label': check['label'], 'passed': False})
        result['passed'] = bool(result['checks']) and all(c['passed'] for c in result['checks'])
    Path('result.json').write_text(json.dumps(result), encoding='utf-8')


if __name__ == '__main__':
    main()
