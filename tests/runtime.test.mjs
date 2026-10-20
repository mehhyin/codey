import test from 'node:test';
import assert from 'node:assert/strict';
import { configureRuntime, executeBrowser, stopRuntime } from '../web/runtime.ts';

test('Python worker errors report the load stage and reject active runs immediately', async t=>{
  const originalWorker=globalThis.Worker,originalFetch=globalThis.fetch;
  let behavior;
  class TestWorker {
    constructor(url){assert.equal(url,'http://localhost/python/worker.js');}
    terminate(){this.terminated=true;}
    postMessage(data){queueMicrotask(()=>behavior(this,data));}
  }
  globalThis.Worker=TestWorker;
  globalThis.fetch=async()=>Response.json({task:{time_limit:20}});
  configureRuntime('http://localhost/python');
  try{
    await t.test('an import failure retains the worker diagnostic',async()=>{
      behavior=(w)=>w.onmessage({data:{type:'failure',error:'Could not load the Python engine: module blocked'}});
      await assert.rejects(executeBrowser('test',{'main.py':''},'run',()=>{}),/module blocked/);
    });
    await t.test('an opaque browser error includes its last startup stage',async()=>{
      behavior=w=>{
        w.onmessage({data:{type:'status',message:'Loading Python libraries…'}});
        w.onerror({message:''});
      };
      await assert.rejects(executeBrowser('test',{'main.py':''},'run',()=>{}),/Loading Python libraries.*Ctrl\+Shift\+R/s);
    });
    await t.test('a crash after initialization does not wait for the execution timeout',async()=>{
      behavior=(w,data)=>data.type==='init'?w.onmessage({data:{type:'ready'}}):w.onerror({message:'Worker crashed'});
      let deadline;
      try{
        await assert.rejects(Promise.race([
          executeBrowser('test',{'main.py':''},'run',()=>{}),
          new Promise((_,reject)=>{deadline=setTimeout(()=>reject(new Error('Did not reject promptly')),1000);}),
        ]),/Worker crashed/);
      }finally{clearTimeout(deadline);}
    });
    await t.test('successful runs still return results and stop the worker',async()=>{
      let usedWorker;
      behavior=(w,data)=>{
        usedWorker=w;
        w.onmessage({data:data.type==='init'?{type:'ready'}:{type:'result',id:data.id,result:{output:'50.0'}}});
      };
      assert.deepEqual(await executeBrowser('test',{'main.py':''},'run',()=>{}),{output:'50.0'});
      assert.equal(usedWorker.terminated,true);
    });
  }finally{stopRuntime();globalThis.Worker=originalWorker;globalThis.fetch=originalFetch;}
});
