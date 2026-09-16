type Reply={type:string;id?:number;result?:any;error?:string;message?:string};
let worker:Worker|undefined,sequence=0;
let active:((value:Reply)=>void)|undefined;
let origin='';
export function configureRuntime(runtimeBaseURL:string){origin=runtimeBaseURL;}
export function stopRuntime(){worker?.terminate();worker=undefined;active=undefined;}
async function startRuntime(onStatus:(text:string)=>void){
  stopRuntime();onStatus('Loading browser Python…');
  worker=new Worker(origin+'/worker.js',{type:'module'});
  await new Promise<void>((resolve,reject)=>{
    const timeout=setTimeout(()=>{stopRuntime();reject(new Error('Browser Python took too long to load. Try again.'));},120000);
    worker!.onmessage=({data}:MessageEvent<Reply>)=>{
      if(data.type==='status')onStatus(data.message||'Loading browser Python…');
      else if(data.type==='ready'){clearTimeout(timeout);resolve();}
      else if(data.type==='failure'&&!data.id){clearTimeout(timeout);stopRuntime();reject(new Error(data.error));}
      else active?.(data);
    };
    worker!.onerror=event=>{clearTimeout(timeout);stopRuntime();reject(new Error(event.message||'Browser Python could not start.'));};
    worker!.postMessage({type:'init'});
  });
}
async function dispatch(type:string,payload:any,seconds:number){
  return new Promise<any>((resolve,reject)=>{
    const id=++sequence;
    const timeout=setTimeout(()=>{stopRuntime();reject(new Error('Time limit reached. Check for an endless loop or a program waiting for input.'));},seconds*1000);
    active=reply=>{
      if(reply.id!==id)return;clearTimeout(timeout);active=undefined;
      if(reply.type==='failure')reject(new Error(reply.error));else resolve(reply.result);
    };
    worker!.postMessage({id,type,payload});
  });
}
export async function executeBrowser(taskId:string,files:Record<string,string>,mode:string,onStatus:(text:string)=>void){
  const response=await fetch('/api/runtime/'+encodeURIComponent(taskId));if(!response.ok)throw new Error('Exercise unavailable.');
  const {task}=await response.json();
  await startRuntime(onStatus);onStatus(mode==='submit'?'Checking your answer…':'Running in browser Python…');
  const result=await dispatch('execute',{task,files,mode},task.time_limit||20);
  if(mode!=='preview')stopRuntime();
  return result;
}
export async function previewRequest(request:unknown){if(!worker)throw new Error('Start the preview again.');return dispatch('preview',request,15);}

// Preview HTML has a separate opaque origin, no network, and no learner scripts.
export function showPreview(container:HTMLElement,page:{html:string;status:number;path:string}){
  const preview=document.createElement('iframe');preview.title='Your Flask app';preview.sandbox.add('allow-scripts','allow-forms');preview.className='flask-preview';
  const doc=new DOMParser().parseFromString(page.html,'text/html');
  doc.querySelectorAll('script,iframe,object,embed,base,meta,link').forEach(el=>el.remove());
  doc.querySelectorAll('*').forEach(el=>{for(const attr of Array.from(el.attributes))if(attr.name.startsWith('on')||['srcdoc','nonce'].includes(attr.name))el.removeAttribute(attr.name);});
  preview.src=origin+'/preview?app='+encodeURIComponent(location.origin);
  const listener=async(event:MessageEvent)=>{
    if(event.source!==preview.contentWindow)return;
    if(event.data?.type==='codey-preview-ready'){preview.contentWindow!.postMessage({type:'codey-render-preview',html:doc.body.innerHTML,path:page.path},'*');return;}
    if(event.data?.type!=='codey-preview')return;
    try{
      const data=event.data;const url=new URL(data.path||page.path,'https://preview.invalid'+page.path);
      if(url.origin!=='https://preview.invalid')throw new Error('Preview links must stay within your app.');
      if(data.method==='GET'&&data.data)for(const [key,value] of Object.entries(data.data))url.searchParams.set(key,String(value));
      const next=await previewRequest({path:url.pathname+url.search,method:data.method==='POST'?'POST':'GET',data:data.data||{}});
      removeEventListener('message',listener);showPreview(container,next);
    }catch(error:any){const p=document.createElement('p');p.textContent=error.message;container.append(p);}
  };
  addEventListener('message',listener);const observer=new MutationObserver(()=>{if(!preview.isConnected){removeEventListener('message',listener);observer.disconnect();}});observer.observe(container,{childList:true});
  container.replaceChildren(preview);
}
