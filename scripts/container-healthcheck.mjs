import { httpProbe } from './http-probe.mjs';
const app=new URL(process.env.BETTER_AUTH_URL);
for(const path of ['/api/health','/python/pyodide/runtime.json']){
  const response=await httpProbe(`http://127.0.0.1:${process.env.PORT||8765}${path}`,app.host);
  if(response.status!==200)throw new Error(`Container health check failed: ${path} returned ${response.status}.`);
  JSON.parse(response.body);
}
