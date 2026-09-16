"""Runs only inside browser WebAssembly. No host filesystem is mounted."""
import base64
import contextlib
import io
import json
import os
import sys
import traceback
from pathlib import Path

class BoundedOutput(io.StringIO):
    def write(self,text):
        super().write(text[:max(0,24000-self.tell())])
        return len(text)

def execute_attempt(payload):
    import uuid
    directory=Path('/attempts')/uuid.uuid4().hex
    directory.mkdir(parents=True)
    os.chdir(directory)
    sys.path.insert(0,str(directory))
    for name in ['practice_api','cleaning','calculations','audit']:
        sys.modules.pop(name,None)
    for name,content in {**payload['task']['files'],**payload['files']}.items():
        target=directory/name
        if not target.resolve().is_relative_to(directory): raise ValueError('Invalid filename')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content,encoding='utf-8')
    if 'practice_api.py' in payload['task']['files']:
        import practice_api
    output,errors=BoundedOutput(),BoundedOutput()
    namespace={'__name__':'__main__','__file__':str(directory/'main.py')}
    result={'output':'','stderr':'','error':None,'checks':[],'passed':False,'artifacts':[]}
    try:
        with contextlib.redirect_stdout(output),contextlib.redirect_stderr(errors):
            exec(payload['task'].get('setup',''),{'__name__':'__fixture__'})
            exec(compile(payload['files'].get('main.py',''),'main.py','exec'),namespace)
        if 'matplotlib.pyplot' in sys.modules:
            plt=sys.modules['matplotlib.pyplot']
            for num in plt.get_fignums()[:4]:
                plt.figure(num).savefig(f'codey-plot-{num}.png',dpi=110,bbox_inches='tight')
    except BaseException as exc:
        if isinstance(exc,SyntaxError): result['error']=f'{type(exc).__name__} on line {exc.lineno}: {exc.msg}'
        else:
            frames=[f for f in traceback.extract_tb(exc.__traceback__) if f.filename=='main.py']
            where=f' on line {frames[-1].lineno}' if frames else ''
            result['error']=f'{type(exc).__name__}{where}: {str(exc)[:1000]}'
    result['output']=output.getvalue()+('\n[Output truncated at 24,000 characters.]' if output.tell()>=24000 else '')
    result['stderr']=errors.getvalue()
    if not result['error'] and payload['mode']=='submit':
        checks_namespace=dict(namespace,__output__=result['output'],__learner_globals__=namespace)
        for check in payload['task']['checks']:
            try:
                with contextlib.redirect_stdout(output),contextlib.redirect_stderr(errors):
                    exec(payload['task'].get('check_imports','')+'\n'+check['code'],checks_namespace)
                passed=True
            except BaseException: passed=False
            result['checks'].append({'label':check['label'],'passed':passed})
        result['passed']=bool(result['checks']) and all(c['passed'] for c in result['checks'])
    if payload['mode']=='preview' and not result['error']:
        app=namespace.get('app')
        if not callable(app): result['error']='Define a Flask application named app. Do not call app.run().'
        else:
            globals()['_preview_client']=app.test_client()
            result['preview']=preview_request({'path':'/'+payload['task'].get('preview_path',''),'method':'GET'})
    names=list(dict.fromkeys([p.name for p in directory.glob('codey-plot-*.png')]+payload['task'].get('exports',[])))
    total=0
    for name in names[:8]:
        target=directory/name
        if not target.is_file() or target.is_symlink() or target.resolve().parent!=directory: continue
        data=target.read_bytes()
        if len(data)>2000000 or total+len(data)>6000000: continue
        mime={'.png':'image/png','.xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','.csv':'text/csv','.json':'application/json','.html':'text/html','.txt':'text/plain'}.get(target.suffix)
        if mime: result['artifacts'].append({'name':name,'mime':mime,'data':base64.b64encode(data).decode()});total+=len(data)
    if result['passed']: result['explanation']=payload['task']['explanation']
    return result

def preview_request(request):
    path=request.get('path','/')
    if not path.startswith('/') or path.startswith('//'): raise ValueError('Use a relative preview path')
    response=_preview_client.open(path,method=request.get('method','GET'),data=request.get('data',{}),follow_redirects=True)
    return {'html':response.get_data(as_text=True)[:500000],'status':response.status_code,'path':response.request.path}
