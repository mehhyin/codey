import { createAuthClient } from 'better-auth/client';
const auth=createAuthClient();
type State={drafts:Record<string,string>;fileDrafts:Record<string,Record<string,string>>;completed:string[];hints:Record<string,number>;last:string|null;blankEditorVersion?:number};
export let account:{id:string;name:string;email:string}|null=null;
export let bootstrap:any;
let revisions:Record<string,number>={},sent:Record<string,string>={},timer:ReturnType<typeof setTimeout>|undefined;
let pending:Record<string,{files:Record<string,string>;revision:number}>={},chain=Promise.resolve();
let metadata:{last:string|null;hints:Record<string,number>}|null=null;
let attempts:any[]=[];
let conflict=false;
let onStatus=(text:string)=>{},onReload=()=>{};
const pendingKey=()=>`codey.pending.${account!.id}`;
export async function request(path:string,body?:unknown,method='POST'){
  const response=await fetch(path,{method:body===undefined?'GET':method,credentials:'same-origin',headers:body===undefined?{}:{'Content-Type':'application/json','X-Codey-Request':'1'},body:body===undefined?undefined:JSON.stringify(body)});
  const data=await response.json();
  if(!response.ok)throw Object.assign(new Error(data.error||'Could not save your work.'),{status:response.status,data});
  return data;
}
export async function initialiseAccount(status:(text:string)=>void,reload:()=>void){
  onStatus=status;onReload=reload;
  bootstrap=await request('/api/bootstrap');account=bootstrap.user;
  return bootstrap;
}
export async function loadAccount():Promise<State>{
  const data=await request('/api/account/workspace');
  const state:State={drafts:{},fileDrafts:{},completed:[],hints:{},last:data.last,blankEditorVersion:1};
  revisions={};sent={};pending={};
  for(const [id,value] of Object.entries(data.drafts) as [string,any][]){
    revisions[id]=value.revision;sent[id]=JSON.stringify(value.files);
    state.drafts[id]=value.files['main.py']||'';
    state.fileDrafts[id]=Object.fromEntries(Object.entries(value.files).filter(([name])=>name!=='main.py')) as Record<string,string>;
  }
  for(const item of data.progress){state.hints[item.exercise_id]=item.hints;if(item.completed_at)state.completed.push(item.exercise_id);}
  try{const recovery=JSON.parse(localStorage.getItem(pendingKey())??localStorage.getItem(`pyroom.pending.${account!.id}`)??'{}');pending=recovery.drafts||recovery;metadata=recovery.metadata||null;attempts=recovery.attempts||[];}catch{pending={};}
  for(const [id,item] of Object.entries(pending)){
    state.drafts[id]=item.files['main.py']||'';state.fileDrafts[id]=Object.fromEntries(Object.entries(item.files).filter(([name])=>name!=='main.py'));
  }
  bootstrap.importedAt=data.importedAt;
  if(metadata){state.last=metadata.last;for(const [id,count] of Object.entries(metadata.hints))state.hints[id]=Math.max(state.hints[id]||0,count);}
  for(const attempt of attempts)if(attempt.result.passed&&!state.completed.includes(attempt.task))state.completed.push(attempt.task);
  if(Object.keys(pending).length)onStatus('Recovered unsaved drafts from this browser.');
  return state;
}
function cachePending(){try{localStorage.setItem(pendingKey(),JSON.stringify({drafts:pending,metadata,attempts}));}catch{onStatus('Local recovery storage is full. Keep this tab open until your account save finishes.');}}
export function hasUnsavedWork(){return Boolean(Object.keys(pending).length||metadata||attempts.length);}
function retry(error:any){onStatus(error.message+' Your work is pending; keep this tab open.');if(!conflict&&(!error.status||error.status>=500)){clearTimeout(timer);timer=setTimeout(()=>void flush().catch(retry),15000);}}
function showConflict(id:string,remote:any){
  conflict=true;
  onStatus('This exercise changed in another tab. Choose which draft to keep.');
  window.dispatchEvent(new CustomEvent('codey-conflict',{detail:{id,
    keepLocal:()=>{conflict=false;pending[id].revision=remote.revision;revisions[id]=remote.revision;cachePending();return flush();},
    useAccount:()=>{conflict=false;delete pending[id];cachePending();onReload();}
  }}));
}
export function queueSave(state:State){
  if(!account)return;
  for(const id of new Set([...Object.keys(state.drafts),...Object.keys(state.fileDrafts)])){
    const files={'main.py':state.drafts[id]||'',...state.fileDrafts[id]};
    if(pending[id]||JSON.stringify(files)!==sent[id])pending[id]={files,revision:pending[id]?.revision??revisions[id]??0};
  }
  metadata={last:state.last,hints:{...state.hints}};
  cachePending();clearTimeout(timer);if(conflict)return;onStatus('Saving to your account…');
  timer=setTimeout(()=>void flush().catch(retry),650);
}
export async function flush(){
  clearTimeout(timer);
  const userId=account?.id;
  const run=async()=>{
    if(!userId||account?.id!==userId)return;
    if(conflict)throw new Error('Resolve the draft conflict before saving.');
    for(const [id,item] of Object.entries({...pending})){
      try{
        const result=await request('/api/account/drafts/'+encodeURIComponent(id),item,'PUT');
        revisions[id]=result.revision;sent[id]=JSON.stringify(item.files);
        if(pending[id]===item)delete pending[id];else if(pending[id])pending[id].revision=result.revision;
        cachePending();
      }catch(error:any){if(error.status===409)showConflict(id,error.data);throw error;}
    }
    const snapshot=metadata;
    if(snapshot){
      if(snapshot.last)await request('/api/account/current',{task:snapshot.last},'PUT');
      for(const [task,count] of Object.entries(snapshot.hints))if(count)await request('/api/account/hints',{task,count});
      if(metadata===snapshot)metadata=null;cachePending();
    }
    for(const attempt of [...attempts]){await request('/api/account/attempts',attempt);attempts=attempts.filter(item=>item.id!==attempt.id);cachePending();}
    onStatus(hasUnsavedWork()?'Saving to your account…':'Saved to your account');
  };
  chain=chain.catch(()=>{}).then(run);return chain;
}
export async function signIn(provider:'google'|'github'){
  const result=await auth.signIn.social({provider,callbackURL:location.origin+'/',errorCallbackURL:location.origin+'/?signin=failed'});
  if(result.error)throw new Error(result.error.message||'Sign-in failed.');
}
export async function signOut(){
  await flush();const result=await auth.signOut();if(result.error)throw new Error(result.error.message||'Sign-out failed.');
  account=null;location.reload();
}
export async function importBrowserProgress(raw:unknown){await flush();return request('/api/account/import',raw);}
export async function saveAttempt(task:string,files:Record<string,string>,result:any){
  if(!account)return;
  const {output,stderr,error,checks,passed}=result;
  attempts.push({id:crypto.randomUUID(),task,files,result:{output:output||'',stderr:stderr||'',error:error||null,checks:checks||[],passed:Boolean(passed)}});cachePending();
  try{await flush();}catch(error){retry(error);throw error;}
}
addEventListener('online',()=>{if(account&&!conflict)void flush().catch(retry);});
