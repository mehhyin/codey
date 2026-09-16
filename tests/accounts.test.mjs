import test from 'node:test';
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { createApp } from '../build/server/app.js';
import { tasks } from '../build/server/course.js';
import { DatabaseSync } from 'node:sqlite';

test('real Better Auth sessions, account isolation, revisions, import, history, and persistence',async()=>{
  const config={baseURL:'http://127.0.0.1:8875',databasePath:'.runtime/auth-test-'+randomUUID()+'.sqlite',secret:'integration-test-only-'+randomUUID()};
  const {app,db}=await createApp(config,{testPassword:true});
  async function call(path,body,cookie='',method='POST',origin=config.baseURL){
    return app.request(config.baseURL+path,{method:body===undefined?'GET':method,headers:{Origin:origin,'Content-Type':'application/json','X-Codey-Request':'1',Cookie:cookie},body:body===undefined?undefined:JSON.stringify(body)});
  }
  async function user(name){
    const response=await call('/api/auth/sign-up/email',{name,email:name+'@example.test',password:'long-test-password-'+name});
    assert.equal(response.status,200,await response.clone().text());
    const cookie=response.headers.getSetCookie().map(c=>c.split(';')[0]).join('; ');assert.ok(cookie);
    return {cookie,data:await response.json()};
  }
  const alice=await user('alice'),bob=await user('bob');
  assert.equal((await call('/api/account/workspace',undefined)).status,401);
  const draft={files:{'main.py':'print("private alice draft")'},revision:0};
  let response=await call('/api/account/drafts/basics-types',draft,alice.cookie,'PUT');assert.equal(response.status,200);
  response=await call('/api/account/drafts/basics-types',draft,alice.cookie,'PUT');assert.equal(response.status,409);
  response=await call('/api/account/drafts/basics-types',{...draft,files:{'../server.ts':'x','main.py':''},revision:1},alice.cookie,'PUT');assert.equal(response.status,400);
  response=await call('/api/account/drafts/basics-types',{...draft,userId:bob.data.user.id},alice.cookie,'PUT');assert.equal(response.status,400);
  const b=await (await call('/api/account/workspace',undefined,bob.cookie)).json();assert.deepEqual(b.drafts,{});
  response=await call('/api/account/drafts/basics-types',draft,alice.cookie,'PUT','https://evil.invalid');assert.equal(response.status,403);
  const imported={drafts:{'basics-types':'should not overwrite','basics-variables':'legacy'},completed:['basics-variables','unknown'],hints:{'basics-variables':2},last:'basics-variables'};
  assert.equal((await call('/api/account/import',imported,alice.cookie)).status,200);
  const again=await (await call('/api/account/import',imported,alice.cookie)).json();assert.equal(again.imported,false);
  const a=await (await call('/api/account/workspace',undefined,alice.cookie)).json();
  assert.equal(a.drafts['basics-types'].files['main.py'],draft.files['main.py']);assert.equal(a.drafts['basics-variables'].files['main.py'],'legacy');
  assert.equal(a.progress[0].completion_source,'browser-import');
  const task=tasks['basics-types'],attemptId=randomUUID();
  const attempt={id:attemptId,task:task.id,files:{'main.py':task.solution},result:{output:'',error:null,checks:task.checks.map(c=>({label:c.label,passed:true})),passed:true}};
  assert.equal((await call('/api/account/attempts',attempt,alice.cookie)).status,200);
  assert.equal((await call('/api/account/attempts',attempt,alice.cookie)).status,200);
  assert.equal((await (await call('/api/account/attempts/'+task.id,undefined,alice.cookie)).json()).attempts.length,1);
  assert.equal((await call('/api/account/attempt/'+attemptId,undefined,bob.cookie)).status,404);
  assert.equal((await call('/api/account/attempt/'+attemptId,undefined,alice.cookie)).status,200);
  assert.equal((await call('/api/account/attempts',attempt,bob.cookie)).status,409);
  assert.equal((await call('/api/account/attempts',{...attempt,files:{'main.py':'changed'}},alice.cookie)).status,409);
  assert.equal((await call('/api/account/attempts',{...attempt,id:randomUUID(),result:{...attempt.result,checks:[]}},alice.cookie)).status,400);
  assert.equal((await call('/api/auth/sign-out',{},alice.cookie)).status,200);
  assert.equal((await call('/api/account/workspace',undefined,alice.cookie)).status,401);
  db.close();
  const stored=new DatabaseSync(config.databasePath);assert.equal(stored.prepare('SELECT COUNT(*) AS n FROM draft').get().n,2);assert.equal(stored.prepare('SELECT COUNT(*) AS n FROM attempt').get().n,1);stored.close();
});

test('normal configuration has no password registration or developer login',async()=>{
  const config={baseURL:'http://127.0.0.1:8877',databasePath:':memory:',secret:'production-shape-test-'+randomUUID()};
  const {app,db}=await createApp(config);
  const response=await app.request(config.baseURL+'/api/auth/sign-up/email',{method:'POST',headers:{Origin:config.baseURL,'Content-Type':'application/json'},body:JSON.stringify({name:'x',email:'x@example.test',password:'something-very-long'})});
  assert.notEqual(response.status,200);
  const bootstrap=await (await app.request(config.baseURL+'/api/bootstrap')).json();assert.equal(bootstrap.user,null);assert.deepEqual(bootstrap.providers,{google:false,github:false});
  assert.equal((await app.request(config.baseURL+'/.env')).status,404);assert.equal((await app.request(config.baseURL+'/data/codey.sqlite')).status,404);
  assert.equal((await app.request(config.baseURL+'/test-login')).status,404);
  db.close();
});
