// Served under /python/. Worker CSP limits connections to that static asset path.
import { loadPyodide } from './pyodide/pyodide.mjs';
const root=new URL('.',import.meta.url).href;
const send=self.postMessage.bind(self);
let py;
self.onmessage=async ({data})=>{
  try{
    if(data.type==='init'){
      send({type:'status',message:'Starting Python…'});
      const manifest=await (await fetch(root+'pyodide/runtime.json')).json();
      py=await loadPyodide({indexURL:root+'pyodide/'});
      send({type:'status',message:'Loading Python libraries…'});
      await py.loadPackage(manifest.packages);
      const micropip=py.pyimport('micropip');
      send({type:'status',message:'Preparing Excel and Flask…'});
      await micropip.install.callKwargs(manifest.wheels.map(name=>root+'pyodide/'+name),{deps:false});
      micropip.destroy();
      py.runPython("import os\nos.environ['MPLBACKEND']='Agg'\nos.environ['MPLCONFIGDIR']='/tmp/matplotlib'\nimport matplotlib\nmatplotlib.use('Agg')");
      py.runPython(await (await fetch(root+'execute.py')).text());
      send({type:'ready'});return;
    }
    py.globals.set('_request_json',JSON.stringify(data.payload));
    const method=data.type==='preview'?'preview_request':'execute_attempt';
    const result=py.runPython(`json.dumps(${method}(json.loads(_request_json)))`);
    send({type:'result',id:data.id,result:JSON.parse(result)});
  }catch(error){send({type:'failure',id:data.id,error:String(error).slice(0,2000)});}
};
