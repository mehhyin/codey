import { Hono } from 'hono';
import { bodyLimit } from 'hono/body-limit';
import { serveStatic } from '@hono/node-server/serve-static';
import { z } from 'zod';
import { readFileSync,existsSync } from 'node:fs';
import { randomUUID } from 'node:crypto';
import { createAuth } from './auth.js';
import { openDatabase,migrateProgress,transaction } from './database.js';
import { modules,tasks,type Task } from './course.js';
import type { Config } from './config.js';
import { runtimeApp } from './runtime-server.js';

const codeFiles=z.record(z.string(),z.string().max(50000)).refine(files=>Object.keys(files).length<=8 && JSON.stringify(files).length<=200000);
const savedDraft=z.object({files:codeFiles,revision:z.number().int().nonnegative()}).strict();
const now=()=>new Date().toISOString();
function validFiles(task:Task,files:Record<string,string>){
  return Object.keys(files).every(name=>name==='main.py'||Object.hasOwn(task.editor_files||{},name)) && Object.hasOwn(files,'main.py');
}

export async function createApp(config:Config,options:{testPassword?:boolean}={}){
  const db=openDatabase(config.databasePath);
  const auth=await createAuth(config,db,options.testPassword===true);
  migrateProgress(db);
  const app=new Hono<{Variables:{userId:string}}>();
  const runtimeBaseURL=config.baseURL+'/python';
  app.use('*',async(c,next)=>{
    if(new URL(c.req.url).host!==new URL(config.baseURL).host)return c.json({error:'Open Codey at its configured address.'},403);
    c.header('X-Content-Type-Options','nosniff');c.header('Referrer-Policy','no-referrer');
    c.header('Content-Security-Policy',`default-src 'self'; script-src 'self'; worker-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'`);
    c.header('Cache-Control','no-store');
    await next();
  });
  app.use('/api/*',bodyLimit({maxSize:10_000_000,onError:c=>c.json({error:'Request is too large.'},413)}));
  app.use('/api/*',async(c,next)=>{
    if(!['GET','HEAD'].includes(c.req.method) && !c.req.path.startsWith('/api/auth/')){
      if(c.req.header('Origin')!==config.baseURL || c.req.header('X-Codey-Request')!=='1' || !c.req.header('Content-Type')?.startsWith('application/json'))return c.json({error:'Refresh Codey before continuing.'},403);
    }
    await next();
  });
  app.on(['GET','POST'],'/api/auth/*',c=>auth.handler(c.req.raw));
  app.get('/api/health',c=>c.json({app:'codey',version:3}));
  app.get('/api/bootstrap',async c=>{
    const session=await auth.api.getSession({headers:c.req.raw.headers});
    return c.json({user:session?{id:session.user.id,name:session.user.name,email:session.user.email}:null,
      providers:{google:Boolean(config.google),github:Boolean(config.github)},runtimeBaseURL,
      runtimeReady:existsSync('.runtime/pyodide/runtime.json')});
  });
  app.route('/python',runtimeApp(config.baseURL));
  app.get('/api/course',c=>c.json({modules}));
  app.get('/api/runtime/:exercise',c=>{
    const task=tasks[c.req.param('exercise')];if(!task)return c.json({error:'Exercise not found.'},404);
    return c.json({task:{id:task.id,files:{...task.files,...(Object.hasOwn(task.files,'practice_api.py')?{'practice_api.py':readFileSync('runner/practice_api.py','utf8')}:{})},
      checks:task.checks,check_imports:task.check_imports,setup:task.setup,exports:task.exports,
      explanation:task.explanation,web_preview:task.web_preview,preview_path:task.preview_path,time_limit:task.time_limit||8}});
  });
  app.post('/api/solution',async c=>{
    const {task:id}=z.object({task:z.string()}).parse(await c.req.json());const task=tasks[id];
    if(!task)return c.json({error:'Exercise not found.'},404);
    const session=await auth.api.getSession({headers:c.req.raw.headers});
    if(session)db.prepare(`INSERT INTO exercise_progress(user_id,exercise_id,solution_revealed_at) VALUES(?,?,?) ON CONFLICT(user_id,exercise_id) DO UPDATE SET solution_revealed_at=COALESCE(solution_revealed_at,excluded.solution_revealed_at)`).run(session.user.id,id,now());
    return c.json({solution:task.solution,files:task.solution_files||{},explanation:task.explanation});
  });
  app.use('/api/account/*',async(c,next)=>{
    const session=await auth.api.getSession({headers:c.req.raw.headers});
    if(!session)return c.json({error:'Sign in to save progress to your account.'},401);
    c.set('userId',session.user.id);await next();
  });
  app.get('/api/account/workspace',c=>{
    const id=c.get('userId');
    const drafts=db.prepare('SELECT exercise_id,files_json,revision FROM draft WHERE user_id=?').all(id) as {exercise_id:string;files_json:string;revision:number}[];
    const progress=db.prepare('SELECT exercise_id,hints,completed_at,completion_source FROM exercise_progress WHERE user_id=?').all(id);
    const workspace=db.prepare('SELECT last_exercise,imported_at FROM workspace WHERE user_id=?').get(id);
    return c.json({drafts:Object.fromEntries(drafts.map(row=>[row.exercise_id,{files:JSON.parse(row.files_json),revision:row.revision}])),progress,last:workspace?.last_exercise||null,importedAt:workspace?.imported_at||null});
  });
  app.put('/api/account/drafts/:exercise',async c=>{
    const id=c.req.param('exercise'),task=tasks[id];if(!task)return c.json({error:'Exercise not found.'},404);
    const body=savedDraft.parse(await c.req.json());if(!validFiles(task,body.files))return c.json({error:'Invalid project files.'},400);
    const result=transaction(db,()=>{
      const old=db.prepare('SELECT revision,files_json FROM draft WHERE user_id=? AND exercise_id=?').get(c.get('userId'),id);
      if((old?.revision??0)!==body.revision)return {conflict:true,revision:old?.revision??0,files:old?JSON.parse(String(old.files_json)):null};
      db.prepare(`INSERT INTO draft VALUES(?,?,?,?,?) ON CONFLICT(user_id,exercise_id) DO UPDATE SET files_json=excluded.files_json,revision=excluded.revision,updated_at=excluded.updated_at`).run(c.get('userId'),id,JSON.stringify(body.files),body.revision+1,now());
      return {conflict:false,revision:body.revision+1};
    });
    return c.json(result,result.conflict?409:200);
  });
  app.put('/api/account/current',async c=>{
    const body=z.object({task:z.string()}).strict().parse(await c.req.json());
    if(!tasks[body.task])return c.json({error:'Exercise not found.'},404);
    db.prepare(`INSERT INTO workspace(user_id,last_exercise,updated_at) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET last_exercise=excluded.last_exercise,updated_at=excluded.updated_at`).run(c.get('userId'),body.task,now());
    return c.json({saved:true});
  });
  app.post('/api/account/hints',async c=>{
    const body=z.object({task:z.string(),count:z.number().int().min(0).max(3)}).strict().parse(await c.req.json());
    if(!tasks[body.task])return c.json({error:'Exercise not found.'},404);
    db.prepare(`INSERT INTO exercise_progress(user_id,exercise_id,hints) VALUES(?,?,?) ON CONFLICT(user_id,exercise_id) DO UPDATE SET hints=MAX(hints,excluded.hints)`).run(c.get('userId'),body.task,body.count);
    return c.json({saved:true});
  });
  app.post('/api/account/attempts',async c=>{
    const body=z.object({id:z.string().uuid(),task:z.string(),files:codeFiles,result:z.object({output:z.string().max(25000),stderr:z.string().max(25000).optional(),error:z.string().max(4000).nullable(),checks:z.array(z.object({label:z.string().max(300),passed:z.boolean()})).max(30),passed:z.boolean()}).strict()}).strict().parse(await c.req.json());
    const task=tasks[body.task];if(!task||!validFiles(task,body.files))return c.json({error:'Invalid exercise or files.'},400);
    if(body.result.checks.length && (body.result.checks.length!==task.checks.length||body.result.checks.some((check,i)=>check.label!==task.checks[i].label)))return c.json({error:'Checks do not match this exercise.'},400);
    const passed=!body.result.error&&body.result.checks.length===task.checks.length&&body.result.checks.every(check=>check.passed);
    if(passed!==body.result.passed)return c.json({error:'Inconsistent practice result.'},400);
    const existing=db.prepare('SELECT user_id,exercise_id,files_json,result_json FROM attempt WHERE id=?').get(body.id);
    if(existing&&(existing.user_id!==c.get('userId')||existing.exercise_id!==body.task||existing.files_json!==JSON.stringify(body.files)||existing.result_json!==JSON.stringify(body.result)))return c.json({error:'Submission identifier already used.'},409);
    transaction(db,()=>{
      db.prepare('INSERT OR IGNORE INTO attempt VALUES(?,?,?,?,?,?,?,?)').run(body.id,c.get('userId'),body.task,JSON.stringify(body.files),JSON.stringify(body.result),Number(passed),'browser-practice',now());
      if(passed)db.prepare(`INSERT INTO exercise_progress(user_id,exercise_id,completed_at,completion_source) VALUES(?,?,?,'browser-practice') ON CONFLICT(user_id,exercise_id) DO UPDATE SET completed_at=COALESCE(completed_at,excluded.completed_at),completion_source='browser-practice'`).run(c.get('userId'),body.task,now());
    });
    return c.json({saved:true,passed});
  });
  app.get('/api/account/attempts/:exercise',c=>{
    const rows=db.prepare('SELECT id,passed,created_at,source FROM attempt WHERE user_id=? AND exercise_id=? ORDER BY created_at DESC LIMIT 30').all(c.get('userId'),c.req.param('exercise'));
    return c.json({attempts:rows});
  });
  app.get('/api/account/attempt/:id',c=>{
    const row=db.prepare('SELECT * FROM attempt WHERE user_id=? AND id=?').get(c.get('userId'),c.req.param('id'));
    if(!row)return c.json({error:'Attempt not found.'},404);
    return c.json({id:row.id,task:row.exercise_id,files:JSON.parse(String(row.files_json)),result:JSON.parse(String(row.result_json)),createdAt:row.created_at});
  });
  app.post('/api/account/import',async c=>{
    const body=z.object({drafts:z.record(z.string(),z.string().max(50000)).default({}),fileDrafts:z.record(z.string(),codeFiles).default({}),completed:z.array(z.string()).max(1000).default([]),hints:z.record(z.string(),z.number().int().min(0).max(3)).default({}),last:z.string().nullable().optional()}).strip().parse(await c.req.json());
    const user=c.get('userId');
    const result=transaction(db,()=>{
      if(db.prepare('SELECT imported_at FROM workspace WHERE user_id=?').get(user)?.imported_at)return {imported:false};
      for(const id of new Set([...Object.keys(body.drafts),...Object.keys(body.fileDrafts)])){
        const task=tasks[id];if(!task)continue;
        const files={'main.py':body.drafts[id]||'',...body.fileDrafts[id]};
        if(!validFiles(task,files))continue;
        db.prepare('INSERT OR IGNORE INTO draft VALUES(?,?,?,?,?)').run(user,id,JSON.stringify(files),1,now());
      }
      for(const id of new Set([...body.completed,...Object.keys(body.hints)])){
        if(!tasks[id])continue;
        db.prepare(`INSERT INTO exercise_progress(user_id,exercise_id,hints,completed_at,completion_source) VALUES(?,?,?,?,?) ON CONFLICT(user_id,exercise_id) DO UPDATE SET hints=MAX(hints,excluded.hints),completed_at=COALESCE(completed_at,excluded.completed_at),completion_source=COALESCE(completion_source,excluded.completion_source)`).run(user,id,body.hints[id]||0,body.completed.includes(id)?now():null,body.completed.includes(id)?'browser-import':null);
      }
      db.prepare(`INSERT INTO workspace VALUES(?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET imported_at=excluded.imported_at,last_exercise=COALESCE(last_exercise,excluded.last_exercise),updated_at=excluded.updated_at`).run(user,body.last&&tasks[body.last]?body.last:null,now(),now());
      return {imported:true};
    });
    return c.json(result);
  });
  app.onError((error,c)=>{
    if(error instanceof z.ZodError||error instanceof SyntaxError)return c.json({error:'Invalid request data.'},400);
    console.error('Request failed:',error.name);return c.json({error:'This request could not finish. Please try again.'},500);
  });
  app.get('/assets/*',serveStatic({root:'./build/web'}));
  app.get('/favicon.svg',serveStatic({root:'./build/web'}));
  app.get('/',serveStatic({path:'./build/web/index.html'}));
  app.notFound(c=>c.json({error:'Not found.'},404));
  return {app,auth,db};
}
