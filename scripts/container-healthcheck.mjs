const app=new URL(process.env.BETTER_AUTH_URL);
for(const path of ['/api/health','/python/pyodide/runtime.json']){
  const response=await fetch(`http://127.0.0.1:${process.env.PORT||8765}${path}`,{headers:{Host:app.host},signal:AbortSignal.timeout(4000)});
  if(!response.ok)throw new Error('Container health check failed.');
  await response.json();
}
