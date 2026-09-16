const appOrigin=new URL(location.href).searchParams.get('app');
let path='/';
addEventListener('message',event=>{
  if(event.source!==parent||event.origin!==appOrigin||event.data?.type!=='codey-render-preview')return;
  document.getElementById('content').innerHTML=event.data.html;path=event.data.path;
});
document.addEventListener('submit',event=>{
  event.preventDefault();const form=event.target;
  parent.postMessage({type:'codey-preview',path:form.getAttribute('action')||path,method:(form.method||'GET').toUpperCase(),data:Object.fromEntries(new FormData(form))},appOrigin);
});
document.addEventListener('click',event=>{
  const link=event.target.closest('a');
  if(link){event.preventDefault();parent.postMessage({type:'codey-preview',path:link.getAttribute('href'),method:'GET'},appOrigin);}
});
parent.postMessage({type:'codey-preview-ready'},appOrigin);
