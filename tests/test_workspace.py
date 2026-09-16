"""Integration tests for blank workspaces, output files, and actual local previews."""
import base64
import io
import json
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import server
from course import MODULES, all_tasks, public_course
from learning_runtime import configure


def main():
    tasks = all_tasks()
    public = public_course()
    assert len([t for m in MODULES for t in m['tasks']]) == len(tasks) == 173
    for module in public:
        for task in module['tasks']:
            assert task['starter'] == ''
            assert all(code == '' for code in task['editor_files'].values())
            assert 'setup' not in task and 'solution_files' not in task
    conversion = next(t for m in public for t in m['tasks'] if t['id']=='basics-conversion')
    assert {row['name'] for row in conversion['input_data']} == {'price_text', 'quantity_text'}
    configure()
    from openpyxl import load_workbook
    task = tasks['capstones-analysis']
    result = server.execute(task, task['solution'], 'submit')
    assert result['passed'], result
    artifacts = {f['name']: f for f in result['artifacts']}
    assert {'report.png','report.xlsx','audit.json'} <= artifacts.keys()
    assert base64.b64decode(artifacts['report.png']['data']).startswith(bytes([137,80,78,71]))
    workbook = load_workbook(io.BytesIO(base64.b64decode(artifacts['report.xlsx']['data'])))
    assert list(workbook['Summary'].values) == [('region','amount'),('north',30),('south',0)]
    task = tasks['engineering-modules']
    assert server.execute(task,task['solution'],'submit',task['solution_files'])['passed']
    assert not server.execute(task,task['solution'],'submit')['passed']
    task = tasks['sql-parameters']
    # This function needs only the supplied connection, not a sqlite3 import.
    assert server.execute(task,task['solution'].replace('import sqlite3\n',''),'submit')['passed']
    task = tasks['automation-copy']
    # A grader import must not silently supply a missing learner dependency.
    broken = task['solution'].replace('from pathlib import Path\n','')
    assert not server.execute(task,broken,'submit')['passed']
    try:
        for task_id in ['flask-route','flask-query','flask-database','flask-forms','capstones-web']:
            task = tasks[task_id]
            preview = server.launch_preview(task,task['solution'])
            with urllib.request.urlopen(preview['url']) as response:
                assert response.status == 200
            if task_id in ('flask-forms','capstones-web'):
                values = {'name':'Mei & Bo'} if task_id=='flask-forms' else {'name':'Tea','quantity':'2'}
                request=urllib.request.Request(preview['url'],data=urllib.parse.urlencode(values).encode())
                with urllib.request.urlopen(request) as response:
                    page=response.read().decode()
                    assert ('Mei &amp; Bo' if task_id=='flask-forms' else 'Tea: 2') in page
                    assert response.url.startswith(preview['url'])
            req=urllib.request.Request(preview['url'],headers={'Origin':'https://example.invalid'})
            try:
                urllib.request.urlopen(req)
            except urllib.error.HTTPError as error:
                assert error.code==403
            else:
                raise AssertionError('Foreign origin was accepted')
        process,directory=server.PREVIEW
    finally:
        server.stop_preview()
    assert process.poll() is not None and not directory.exists()

    httpd=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
    threading.Thread(target=httpd.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{httpd.server_port}'
    def post(path,body,expected=200,headers=None):
        request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers=headers or {'Content-Type':'application/json','X-Pyroom-Token':server.TOKEN})
        try:
            with urllib.request.urlopen(request) as response:
                assert response.status==expected
                return json.load(response)
        except urllib.error.HTTPError as error:
            assert error.code==expected,(error.code,error.read())
    try:
        with urllib.request.urlopen(base+'/api/course') as response:
            assert len(json.load(response)['modules'])==19
        task=tasks['engineering-modules']
        body={'task':task['id'],'code':task['solution'],'files':task['solution_files'],'mode':'submit'}
        assert post('/api/execute',body)['passed']
        post('/api/execute',dict(body,files={'../unexpected.py':'pass'}),400)
        post('/api/execute',body,403,{'Content-Type':'application/json'})
        post('/api/execute',body,403,{'Content-Type':'application/json','X-Pyroom-Token':server.TOKEN,'Origin':'https://example.invalid'})
        post('/api/execute',dict(body,mode='unknown'),400)
        post('/api/preview',body,400)
        assert post('/api/solution',{'task':task['id']})['files']==task['solution_files']
    finally:
        httpd.shutdown()
        httpd.server_close()
    print('Blank editors, input references, chart/Excel downloads, companion files, local preview GET/POST/redirect/persistence, cleanup, and HTTP validation passed.')


if __name__=='__main__':
    main()
