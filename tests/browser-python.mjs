import { loadPyodide } from 'pyodide';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import assert from 'node:assert/strict';
const root=resolve('.runtime/pyodide')+'/';
const manifest=JSON.parse(readFileSync(root+'runtime.json','utf8'));
const py=await loadPyodide({indexURL:root});
await py.loadPackage(manifest.packages);
for(const name of manifest.wheels){py.unpackArchive(new Uint8Array(readFileSync(root+name)),'zip',{extractDir:py.runPython('import site;site.getsitepackages()[0]')});}
py.runPython("import os\nos.environ['MPLBACKEND']='Agg'\nimport matplotlib\nmatplotlib.use('Agg')");
py.runPython(readFileSync('runner/execute.py','utf8'));
const tasks=JSON.parse(readFileSync('.generated/tasks.json','utf8'));
let failures=0;
for(const task of Object.values(tasks)){
 if(task.files['practice_api.py'])task.files['practice_api.py']=readFileSync('runner/practice_api.py','utf8');
 const files={'main.py':task.solution,...task.solution_files};
 py.globals.set('_request_json',JSON.stringify({task,files,mode:'submit'}));
 try{
   const result=JSON.parse(py.runPython('json.dumps(execute_attempt(json.loads(_request_json)))'));
   if(!result.passed){failures++;console.log('FAIL',task.id,result.error,result.checks.filter(c=>!c.passed));}else console.log('PASS',task.id);
 }catch(error){failures++;console.log('FAIL',task.id,String(error).slice(-1200));}
 py.runPython("import matplotlib.pyplot as plt\nplt.close('all')");
}
const task=tasks['flask-tracker-project'];
py.globals.set('_request_json',JSON.stringify({task,files:{'main.py':task.solution},mode:'preview'}));
const preview=JSON.parse(py.runPython('json.dumps(execute_attempt(json.loads(_request_json)))'));assert.ok(preview.preview?.html.includes('<form'),preview.error);
py.globals.set('_request_json',JSON.stringify({path:'/',method:'POST',data:{title:'A browser task'}}));
assert.ok(JSON.parse(py.runPython('json.dumps(preview_request(json.loads(_request_json)))')).html.includes('A browser task'));
console.log(`${Object.keys(tasks).length} browser-Python solutions; ${failures} failures. Flask form preview checked.`);
process.exitCode=failures?1:0;
