import { Hono } from 'hono';
import { serveStatic } from '@hono/node-server/serve-static';
import { readFileSync } from 'node:fs';

export function runtimeApp(appOrigin:string){
  const app=new Hono();
  const assets=appOrigin+'/python/';
  app.use('*',async(c,next)=>{
    // TLS terminates at the reverse proxy; it must preserve the configured Host.
    if(new URL(c.req.url).host!==new URL(appOrigin).host)return c.text('Invalid runtime origin',403);
    // Only static assets live here. The worker policy cannot fetch account routes.
    c.header('Access-Control-Allow-Origin','*');c.header('Cross-Origin-Resource-Policy','cross-origin');
    c.header('X-Content-Type-Options','nosniff');c.header('Referrer-Policy','no-referrer');
    c.header('Cache-Control','no-cache');
    c.header('Content-Security-Policy',`default-src 'none'; script-src ${assets} 'wasm-unsafe-eval'; worker-src 'none'; connect-src ${assets}; style-src 'none'; frame-ancestors ${appOrigin}; base-uri 'none'; form-action 'none'`);
    await next();
  });
  app.get('/preview',c=>{
    if(c.req.query('app')!==appOrigin)return c.text('Invalid application',403);
    c.header('Content-Security-Policy',`default-src 'none'; script-src ${assets}; style-src 'unsafe-inline'; frame-ancestors ${appOrigin}; base-uri 'none'; form-action 'none'`);
    return c.html('<!doctype html><meta charset="utf-8"><style>body{font:16px/1.6 system-ui;padding:18px;background:white;color:#222}input,button{font:inherit;margin:5px;padding:5px}</style><main id="content"></main><script src="/python/preview.js"></script>');
  });
  for(const file of ['worker.js','preview.js','execute.py'])app.get('/'+file,c=>c.body(readFileSync('runner/'+file),200,{'Content-Type':file.endsWith('.js')?'text/javascript':'text/plain'}));
  app.get('/pyodide/*',serveStatic({root:'.runtime',rewriteRequestPath:path=>path.replace(/^\/python\//,'/')}));
  return app;
}
