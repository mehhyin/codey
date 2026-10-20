// Served under /python/. Worker CSP limits connections to that static asset path.
const root=new URL('.',import.meta.url).href;
const send=self.postMessage.bind(self);
let py;
let stage='starting Python';
async function runtimeFile(path){
  const response=await fetch(root+path);
  if(!response.ok)throw new Error(`Could not load ${path} (HTTP ${response.status}).`);
  return response;
}
self.onmessage=async ({data})=>{
  try{
    if(data.type==='init'){
      // Import inside the handler so module-load failures reach the console.
      stage='loading the Python engine';
      send({type:'status',message:'Loading the Python engine…'});
      const { loadPyodide }=await import('./pyodide/pyodide.mjs');
      stage='starting Python';
      send({type:'status',message:'Starting Python…'});
      const manifest=await (await runtimeFile('pyodide/runtime.json')).json();
      py=await loadPyodide({indexURL:root+'pyodide/'});
      stage='loading Python libraries';
      send({type:'status',message:'Loading Python libraries…'});
      await py.loadPackage(manifest.packages);
      const micropip=py.pyimport('micropip');
      stage='preparing Excel and Flask';
      send({type:'status',message:'Preparing Excel and Flask…'});
      await micropip.install.callKwargs(manifest.wheels.map(name=>root+'pyodide/'+name),{deps:false});
      micropip.destroy();
      py.runPython("import os\nos.environ['MPLBACKEND']='Agg'\nos.environ['MPLCONFIGDIR']='/tmp/matplotlib'\nimport matplotlib\nmatplotlib.use('Agg')");
      stage='preparing the exercise runner';
      py.runPython(await (await runtimeFile('execute.py')).text());
      send({type:'ready'});return;
    }
    py.globals.set('_request_json',JSON.stringify(data.payload));
    const method=data.type==='preview'?'preview_request':'execute_attempt';
    const result=py.runPython(`json.dumps(${method}(json.loads(_request_json)))`);
    send({type:'result',id:data.id,result:JSON.parse(result)});
  }catch(error){send({type:'failure',id:data.id,error:(data.type==='init'?`Browser Python failed while ${stage}. `:'')+String(error).slice(0,2000)});}
};
