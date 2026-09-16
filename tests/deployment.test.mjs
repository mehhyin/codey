import test from 'node:test';
import assert from 'node:assert/strict';
import { configFromEnvironment } from '../build/server/config.js';
import { createApp } from '../build/server/app.js';
const secret='deployment-test-secret-only-123456789';
test('one container port supports a public HTTPS domain and local development',()=>{
  const c=configFromEnvironment({BETTER_AUTH_SECRET:secret,BETTER_AUTH_URL:'https://codey.john.shiksha',HOST:'0.0.0.0',PORT:'8765'});
  assert.equal(c.port,8765);assert.equal(c.host,'0.0.0.0');assert.equal(c.baseURL,'https://codey.john.shiksha');
  const local=configFromEnvironment({BETTER_AUTH_SECRET:secret});assert.equal(local.host,'127.0.0.1');
  for(const invalid of [{BETTER_AUTH_URL:'http://192.168.1.10:8765'},{BETTER_AUTH_URL:'https://learn.example.test/'},{PORT:'0'},{PORT:'invalid'}])
    assert.throws(()=>configFromEnvironment({BETTER_AUTH_SECRET:secret,...invalid}));
});
test('Cloudflare HTTP upstream preserves secure cookies, host validation and worker CSP',async()=>{
  const baseURL='https://codey.john.shiksha';
  const {app,db}=await createApp({baseURL,secret,databasePath:':memory:'},{testPassword:true});
  try{
    const bootstrap=await app.request('http://codey.john.shiksha/api/bootstrap');
    assert.equal(bootstrap.status,200);assert.equal((await bootstrap.json()).runtimeBaseURL,baseURL+'/python');
    assert.equal((await app.request('http://wrong.example.test/api/health',{headers:{'X-Forwarded-Host':'codey.john.shiksha'}})).status,403);
    const response=await app.request('http://codey.john.shiksha/api/auth/sign-up/email',{method:'POST',headers:{Origin:baseURL,'Content-Type':'application/json'},body:JSON.stringify({name:'TLS test',email:'tls@example.test',password:'test-only-password-1234'})});
    assert.equal(response.status,200,await response.clone().text());
    assert.ok(response.headers.getSetCookie().some(c=>/HttpOnly/i.test(c)&&/; Secure/i.test(c)));
    const worker=await app.request('http://codey.john.shiksha/python/worker.js');assert.equal(worker.status,200);
    const policy=worker.headers.get('content-security-policy');
    assert.match(policy,/connect-src https:\/\/codey.john.shiksha\/python\/;/);
    assert.match(policy,/worker-src 'none'/);assert.ok(!policy.includes("'unsafe-eval'"));
    assert.equal((await app.request('http://codey.john.shiksha/python/pyodide/runtime.json')).status,200);
    assert.equal((await app.request('http://codey.john.shiksha/python/api/account/workspace')).status,404);
    assert.equal((await app.request('http://codey.john.shiksha/python/preview?app='+encodeURIComponent(baseURL))).status,200);
    assert.equal((await app.request('http://codey.john.shiksha/api/account/workspace')).status,401);
  }finally{db.close();}
});
