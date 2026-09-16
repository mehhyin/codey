import concurrent.futures
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP))
from course import MODULES, all_tasks, public_course
from server import execute


def check_solution(task):
    result = execute(task, task['solution'], 'submit', task.get('solution_files'))
    if not result.get('passed'):
        return task['id'], result
    if execute(task, '', 'submit').get('passed'):
        return task['id'], 'Empty answer incorrectly passed'
    return task['id'], None


if __name__ == '__main__':
    tasks = list(all_tasks().values())
    assert len(tasks) == len(set(t['id'] for t in tasks))
    assert len(MODULES) == 19
    assert len(tasks) == 173
    assert all(len(m['tasks']) >= 3 and m['reference'] for m in MODULES)
    assert all(len(t['hints']) == 3 and t['checks'] for t in tasks)
    assert all('solution' not in t and 'explanation' not in t for m in public_course() for t in m['tasks'])
    assert all(t['walkthrough'] and t['pitfall'] for t in tasks if t['kind'] in ('practice', 'debug', 'checkpoint') and 'review' not in t)
    for task in tasks:
        assert all(id in all_tasks() for id in task.get('review', [])), task['id']
        for filename, code in task.get('solution_files', {}).items():
            compile(code, filename, 'exec')
        compile(task['solution'], task['id'], 'exec')
        for check in task['checks']:
            compile(check['code'], task['id'] + ':check', 'exec')
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for id, problem in pool.map(check_solution, tasks):
            print(('FAIL' if problem else 'PASS'), id, problem or '', flush=True)
            if problem:
                failures.append((id, problem))
    sample = tasks[0]
    assert not execute(sample, 'total = 0', 'submit')['passed']
    assert 'SyntaxError' in execute(sample, 'if :', 'run')['error']
    assert 'NameError' in execute(sample, 'print(missing_name)', 'run')['error']
    assert 'Time limit' in execute(sample, 'while True: pass', 'run')['error']
    output = execute(sample, 'print("a" * 50000)', 'run')['output']
    assert len(output) < 25000 and 'truncated' in output
    assert execute(sample, 'print(2 + 3)', 'run')['output'].strip() == '5'
    print(f'{len(tasks)} worked solutions; {len(failures)} failures. Error, timeout, output, and wrong-answer checks passed.', flush=True)
    raise SystemExit(bool(failures))
