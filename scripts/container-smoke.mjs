import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
import assert from 'node:assert/strict';
import { httpProbe } from './http-probe.mjs';
const name='codey-smoke-'+randomUUID(),volume=name+'-data',image=process.argv[2]||'codey:ci';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8'}).trim();
const probe=(path,host='codey.example.test')=>httpProbe('http://127.0.0.1:18765'+path,host,1000);
try{
  docker('volume','create',volume);
  docker('run','-d','--name',name,'-p','127.0.0.1:18765:8765','-v',volume+':/data',
    '-e','BETTER_AUTH_URL=https://codey.example.test',image);
  async function ready(){
    let failure='no response';
    for(let n=0;n<40;n++){
      try{const r=await probe('/api/health');if(r.status===200)return;failure=`HTTP ${r.status}`;}catch(error){failure=error.message;}
      await new Promise(resolve=>setTimeout(resolve,500));
    }
    throw new Error('Container did not become ready: '+failure);
  }
  await ready();
  docker('exec',name,'node','scripts/container-healthcheck.mjs');
  assert.equal(docker('exec',name,'id','-u'),'99');
  const r=await probe('/api/bootstrap');
  const body=JSON.parse(r.body);assert.equal(body.runtimeBaseURL,'https://codey.example.test/python');assert.equal(body.runtimeReady,true);
  assert.equal((await probe('/api/health','wrong.example.test')).status,403);
  assert.equal((await probe('/python/api/account/workspace')).status,404);
  assert.equal((await probe('/.env')).status,404);
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
