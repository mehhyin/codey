import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import assert from 'node:assert/strict';
const name='codey-smoke-'+randomUUID(),volume=name+'-data',image=process.argv[2]||'codey:ci';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8'}).trim();
try{
  docker('volume','create',volume);
  docker('run','-d','--name',name,'-p','127.0.0.1:18765:8765','-v',volume+':/data',
    '-e','BETTER_AUTH_URL=https://codey.example.test',image);
  async function ready(){
    for(let n=0;n<40;n++){
      try{const r=await fetch('http://127.0.0.1:18765/api/health',{headers:{Host:'codey.example.test'},signal:AbortSignal.timeout(1000)});if(r.ok)return;}catch{}
      await new Promise(resolve=>setTimeout(resolve,500));
    }
    throw new Error('Container did not become ready.');
  }
  await ready();
  docker('exec',name,'node','scripts/container-healthcheck.mjs');
  assert.equal(docker('exec',name,'id','-u'),'99');
  const r=await fetch('http://127.0.0.1:18765/api/bootstrap',{headers:{Host:'codey.example.test'}});
  const body=await r.json();assert.equal(body.runtimeBaseURL,'https://codey.example.test/python');assert.equal(body.runtimeReady,true);
  assert.equal((await fetch('http://127.0.0.1:18765/api/health',{headers:{Host:'wrong.example.test'}})).status,403);
  assert.equal((await fetch('http://127.0.0.1:18765/python/api/account/workspace',{headers:{Host:'codey.example.test'}})).status,404);
  assert.equal((await fetch('http://127.0.0.1:18765/.env',{headers:{Host:'codey.example.test'}})).status,404);
  const exec=code=>docker('exec',name,'node','--input-type=module','-e',code);
  exec("import {DatabaseSync} from 'node:sqlite';const db=new DatabaseSync('/data/codey.sqlite');db.exec('CREATE TABLE smoke_marker(value INTEGER); INSERT INTO smoke_marker VALUES(42)');db.close();");
  const secretDigest=exec("import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';console.log(createHash('sha256').update(readFileSync('/data/auth-secret')).digest('hex'));");
  docker('restart',name);await ready();
  assert.equal(exec("import {DatabaseSync} from 'node:sqlite';const db=new DatabaseSync('/data/codey.sqlite');console.log(db.prepare('SELECT value FROM smoke_marker').get().value);db.close();"),'42');
  assert.equal(exec("import {readFileSync} from 'node:fs';import {createHash} from 'node:crypto';console.log(createHash('sha256').update(readFileSync('/data/auth-secret')).digest('hex'));"),secretDigest);
  docker('exec',name,'node','scripts/container-entrypoint.mjs','backup');
  docker('stop',name);assert.equal(docker('inspect','--format','{{.State.ExitCode}}',name),'0');
  console.log('Container smoke checks passed: non-root, proxy routing, isolation, restart, database, secret and backup.');
}catch(error){try{console.error(docker('logs',name));}catch{}throw error;}
finally{try{docker('rm','-f',name);}catch{}try{docker('volume','rm',volume);}catch{}}
