'use strict';
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const key = 'pyroom.workspace.v1';
let modules = [], tasks = [], token = '', current, busy = false, state = {drafts:{}, completed:[], hints:{}, last:null};
let dialogAction = null;
function save() { try {localStorage.setItem(key, JSON.stringify(state)); $('saved-label').textContent='Draft saved on this device';} catch { $('storage-warning').hidden=false; $('storage-warning').textContent='Browser storage is unavailable or full. Your work will last only for this visit.'; $('saved-label').textContent='Draft held for this visit'; } }
function highlight(code) {
  const re = /#[^\n]*|(?:f|r|b)?"(?:\\.|[^"\\])*"|(?:f|r|b)?'(?:\\.|[^'\\])*'|\b(?:def|return|if|elif|else|for|while|in|not|and|or|True|False|None|import|from|as|with|try|except|raise|class|pass|break|continue|lambda|is)\b|\b(?:print|len|sum|int|float|str|list|dict|set|range|enumerate|sorted|round|open|min|max|zip|isinstance|abs)\b|\b\d+(?:\.\d+)?\b/g;
  let result='', end=0;
  for (const m of code.matchAll(re)) {result+=esc(code.slice(end,m.index));const v=m[0]; const type=v.startsWith('#')?'comment':/^[frb]?["']/.test(v)?'string':/^\d/.test(v)?'number':/^(print|len|sum|int|float|str|list|dict|set|range|enumerate|sorted|round|open|min|max|zip|isinstance|abs)$/.test(v)?'builtin':'keyword';result+=`<span class="tok-${type}">${esc(v)}</span>`;end=m.index+v.length;}
  return result+esc(code.slice(end));
}
function paintEditor(){const code=$('editor').value;$('highlight').innerHTML=highlight(code)+'\n';$('line-numbers').textContent=Array.from({length:code.split('\n').length},(_,i)=>i+1).join('\n');syncScroll();}
function syncScroll(){$('highlight').scrollTop=$('editor').scrollTop;$('highlight').scrollLeft=$('editor').scrollLeft;$('line-numbers').scrollTop=$('editor').scrollTop;}
function persistDraft(){if(current){state.drafts[current.id]=$('editor').value;save();}paintEditor();}
function renderNav(){
  $('course-nav').innerHTML=modules.map((m,i)=>`<details class="module" ${m.tasks.some(t=>t.id===current?.id)?'open':''}><summary><span class="module-number">${String(i+1).padStart(2,'0')}</span><span class="module-name">${esc(m.title)}</span><span class="module-count">${m.tasks.filter(t=>state.completed.includes(t.id)).length}/${m.tasks.length}</span><span class="module-chevron">›</span></summary>${m.tasks.map((t,j)=>`${t.kind==='project'&&m.tasks[j-1]?.kind!=='project'?'<div class="project-divider">GUIDED PROJECT</div>':''}<button class="task-link ${t.id===current?.id?'active':''} ${state.completed.includes(t.id)?'done':''}" data-task="${t.id}" ${t.id===current?.id?'aria-current="step"':''}><span class="task-icon">${state.completed.includes(t.id)?'✓':t.kind==='project'?'◇':'○'}</span><span>${esc(t.title)}</span></button>`).join('')}</details>`).join('');
  const count=state.completed.filter(id=>tasks.some(t=>t.id===id)).length,percent=Math.round(count/tasks.length*100);
  $('progress-text').textContent=`${count} of ${tasks.length} completed`;$('progress-percent').textContent=`${percent}%`;$('progress').value=percent;
}
function checksView(checks){$('checks').innerHTML=checks.map(c=>`<div class="check-item"><span class="${c.passed===true?'pass':c.passed===false?'fail':'pending'}">${c.passed===true?'✓':c.passed===false?'×':'○'}</span><span>${esc(c.label)}</span></div>`).join('');}
function showTab(name){for(const n of ['console','checks']){$(n+'-panel').hidden=n!==name;$(n+'-tab').classList.toggle('active',n===name);$(n+'-tab').setAttribute('aria-selected',String(n===name));$(n+'-tab').tabIndex=n===name?0:-1;}}
function renderHints(){const count=state.hints[current.id]||0;$('hints').innerHTML=current.hints.slice(0,count).map((h,i)=>`<p><strong>Hint ${i+1}.</strong> ${esc(h)}</p>`).join('');$('hint-counter').textContent=`${count} / ${current.hints.length}`;$('hint-btn').disabled=count>=current.hints.length;$('hint-btn').innerHTML=count>=current.hints.length?'All hints revealed':'Reveal a hint <span>+</span>';}
function teachingNotes(t) {
  if (!t.walkthrough) return '';
  return `<details class="teaching-notes"><summary>Walk through the example</summary><ol>${t.walkthrough.map(step=>`<li>${esc(step)}</li>`).join('')}</ol></details>`;
}
function referencePanel(m, t) {
  const pitfall=t.pitfall?`<div class="pitfall"><strong>A common mistake</strong><p>${esc(t.pitfall)}</p></div>`:'';
  return pitfall + `<details class="module-reference"><summary>Keep this reference handy <span>${esc(m.title)}</span></summary><div>${(m.reference||[]).map(([title,code,explanation])=>`<section><h3>${esc(title)}</h3><pre>${highlight(code)}</pre><p>${esc(explanation)}</p></section>`).join('')}</div></details>`;
}
function selectTask(id){
  if(busy)return;const t=tasks.find(t=>t.id===id);if(!t)return;current=t;state.last=id;save();
  const m=modules.find(m=>m.tasks.includes(t)),i=m.tasks.indexOf(t);
  $('breadcrumb').innerHTML=`${esc(m.title)} <span>/</span> ${({project:'Project',practice:'Practice',debug:'Debugging',checkpoint:'Checkpoint'})[t.kind]||'Lesson'} ${i+1} of ${m.tasks.length}`;$('duration').textContent=`${t.minutes} min`;
  $('lesson-content').innerHTML=`<div class="lesson-number">${({project:'BUILD SOMETHING',practice:'BUILD CONFIDENCE',debug:'FIND & FIX',checkpoint:'CHECK YOUR UNDERSTANDING'})[t.kind]||'LEARN BY DOING'} <span class="type">/ ${String(i+1).padStart(2,'0')}</span></div><h1>${esc(t.title)}</h1><p class="concept">${esc(t.concept)}</p><div class="example"><div class="example-label"><span>A small example</span><span>Python</span></div><pre>${highlight(t.example)}</pre></div>${teachingNotes(t)}<div class="goal-heading"><span class="target-icon">◎</span><h3>Your turn</h3></div><ol class="goal-list">${t.goal.map(g=>`<li>${esc(g)}</li>`).join('')}</ol>${Object.keys(t.files).length?`<details class="files"><summary>Sample files · ${Object.keys(t.files).length} available</summary>${Object.entries(t.files).map(([name,data])=>`<div class="file-name">${esc(name)}</div><pre class="file-data">${esc(data)}</pre>`).join('')}</details>`:''}<div class="check-preview"><span>✓</span> ${t.checks.length} checks to help you get there</div>`;
  $('lesson-content').insertAdjacentHTML('beforeend', referencePanel(m, t));
  $('editor').value=state.drafts[id]??t.starter;paintEditor();$('editor').scrollTop=0;syncScroll();
  $('solution').hidden=true;$('solution').innerHTML='';$('solution-btn').disabled=false;$('success').hidden=true;$('output').hidden=true;$('console-empty').hidden=false;$('run-status').textContent='Ready when you are';$('check-count').textContent='';checksView(t.checks.map(label=>({label})));showTab('console');renderHints();renderNav();
  $('previous').disabled=tasks.indexOf(t)===0;$('next').disabled=tasks.indexOf(t)===tasks.length-1;document.querySelector('.lesson-pane').scrollTop=0;
}
async function api(path,body){const response=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-Pyroom-Token':token},body:JSON.stringify(body)});const data=await response.json();if(!response.ok)throw new Error(data.error||'Something went wrong.');return data;}
function setBusy(value){busy=value;for(const id of ['run-btn','submit-btn','reset-btn'])$(id).disabled=value;$('editor').readOnly=value;$('previous').disabled=value||tasks.indexOf(current)===0;$('next').disabled=value||tasks.indexOf(current)===tasks.length-1;for(const button of document.querySelectorAll('[data-task]'))button.disabled=value;$('submit-btn').innerHTML=value?'Working…':'Submit answer <span>→</span>';}
async function run(mode){
  if(busy||!current)return;persistDraft();setBusy(true);$('run-status').textContent=mode==='submit'?'Checking your answer…':'Running…';$('success').hidden=true;
  try{const result=await api('/api/execute',{task:current.id,code:$('editor').value,mode});
    const text=[result.output,result.stderr,result.error].filter(Boolean).join('\n');$('console-empty').hidden=true;$('output').hidden=false;$('output').textContent=text||'Finished successfully. Use print() to display a value.';$('output').classList.toggle('output-error',!!result.error);
    checksView(result.checks?.length?result.checks:current.checks.map(label=>({label})));
    $('check-count').textContent=result.checks?.length?`${result.checks.filter(c=>c.passed).length}/${result.checks.length}`:'';
    if(result.error){$('run-status').textContent='Needs another look';showTab('console');}
    else if(mode==='run'){$('run-status').textContent='Run finished · submit to check';showTab('console');}
    else if(result.passed){if(!state.completed.includes(current.id))state.completed.push(current.id);save();renderNav();$('run-status').textContent='All checks passed';$('success').hidden=false;$('success').innerHTML=`<h3>${state.completed.length===tasks.length?'Course complete. Nicely done.':'You’ve got it.'}</h3><p>${esc(result.explanation)}</p>`;showTab('checks');}
    else{$('run-status').textContent='Keep going · hints are available';showTab('checks');}
    return result;
  }catch(err){$('console-empty').hidden=true;$('output').hidden=false;$('output').classList.add('output-error');$('output').textContent=`Could not run your code. ${err.message} If Pyroom was closed, reopen Start Pyroom.cmd.`;$('run-status').textContent='Connection problem';showTab('console');}
  finally{setBusy(false);}
}
function confirmAction(title,copy,label,action){$('dialog-title').textContent=title;$('dialog-copy').textContent=copy;$('dialog-confirm').textContent=label;dialogAction=action;$('confirm-dialog').showModal();}
$('dialog-cancel').onclick=()=>{$('confirm-dialog').close();dialogAction=null;};$('dialog-confirm').onclick=()=>{$('confirm-dialog').close();const action=dialogAction;dialogAction=null;action?.();};
$('course-nav').onclick=e=>{const b=e.target.closest('[data-task]');if(b)selectTask(b.dataset.task);};
$('course-toggle').onclick=()=>{const hidden=document.querySelector('.workspace').classList.toggle('sidebar-hidden');$('course-toggle').setAttribute('aria-expanded',String(!hidden));};
$('editor').addEventListener('input',persistDraft);$('editor').addEventListener('scroll',syncScroll);
$('editor').addEventListener('keydown',e=>{
  const editor=e.target;if(busy)return;
  if(e.key==='Tab'){e.preventDefault();const start=editor.selectionStart,end=editor.selectionEnd;editor.setRangeText('    ',start,end,'end');persistDraft();}
  if(e.key==='Enter'&&!e.ctrlKey&&!e.metaKey){e.preventDefault();const before=editor.value.slice(0,editor.selectionStart),line=before.split('\n').pop(),indent=(line.match(/^\s*/)||[''])[0]+(line.trimEnd().endsWith(':')?'    ':'');editor.setRangeText('\n'+indent,editor.selectionStart,editor.selectionEnd,'end');persistDraft();}
});
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&!$('confirm-dialog').open){e.preventDefault();run(e.shiftKey?'submit':'run');}});
$('run-btn').onclick=()=>run('run');$('submit-btn').onclick=()=>run('submit');
for(const name of ['console','checks']){$(name+'-tab').onclick=()=>showTab(name);$(name+'-tab').onkeydown=e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const other=name==='console'?'checks':'console';showTab(other);$(other+'-tab').focus();}};}
$('previous').onclick=()=>selectTask(tasks[tasks.indexOf(current)-1]?.id);$('next').onclick=()=>selectTask(tasks[tasks.indexOf(current)+1]?.id);
$('hint-btn').onclick=()=>{state.hints[current.id]=Math.min((state.hints[current.id]||0)+1,current.hints.length);save();renderHints();};
$('reset-btn').onclick=()=>confirmAction('Reset this code?','This replaces your draft for this exercise with its starting code. Your completed lessons and hints stay saved.','Reset code',()=>{$('editor').value=current.starter;persistDraft();});
$('solution-btn').onclick=()=>confirmAction('Reveal the worked solution?','You can compare it with your approach. Revealing a solution does not mark the exercise complete.','Reveal solution',async()=>{const id=current.id;try{const data=await api('/api/solution',{task:id});if(current.id!==id)return;$('solution').hidden=false;$('solution').innerHTML=`<p class="solution-label">One way to solve it</p><pre class="solution-code">${highlight(data.solution)}</pre><p>${esc(data.explanation)}</p>`;$('solution-btn').disabled=true;}catch(err){$('run-status').textContent=err.message;}});
async function init(){
  try{const raw=JSON.parse(localStorage.getItem(key)||'null');if(raw&&typeof raw==='object'){state.drafts=Object.fromEntries(Object.entries(raw.drafts||{}).filter(([k,v])=>typeof v==='string'));state.completed=Array.isArray(raw.completed)?raw.completed.filter(x=>typeof x==='string'):[];state.hints=Object.fromEntries(Object.entries(raw.hints||{}).filter(([k,v])=>Number.isInteger(v)&&v>=0&&v<=3));state.last=typeof raw.last==='string'?raw.last:null;}}catch{}
  try{const response=await fetch('/api/course');if(!response.ok)throw new Error('Unable to load the course.');const data=await response.json();modules=data.modules;token=data.token;tasks=modules.flatMap(m=>m.tasks);selectTask(tasks.find(t=>t.id===state.last)?.id||tasks[0].id);if(matchMedia('(max-width:640px)').matches){document.querySelector('.workspace').classList.add('sidebar-hidden');$('course-toggle').setAttribute('aria-expanded','false');}
    const context=document.modelContext;if(context?.registerTool){try{await context.registerTool({name:'get_learning_progress',description:'Read this local Python course and completed exercise IDs.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:async()=>({current:current.id,completed:[...state.completed],total:tasks.length})});await context.registerTool({name:'open_python_exercise',description:'Navigate to an exercise. Saves existing work; does not run code.',inputSchema:{type:'object',properties:{id:{type:'string'}},required:['id'],additionalProperties:false},annotations:{readOnlyHint:false},execute:async input=>{if(busy||!input||typeof input.id!=='string'||!tasks.some(t=>t.id===input.id))throw new Error('Exercise unavailable');selectTask(input.id);return {current:current.id};}});}catch{}}
  }catch(err){$('lesson-content').innerHTML=`<h1>Let’s reconnect.</h1><p class="concept">${esc(err.message)} Open Start Pyroom.cmd and refresh this page.</p>`;for(const id of ['run-btn','submit-btn','hint-btn','solution-btn','reset-btn','previous','next'])$(id).disabled=true;}
}
init();
