// Local UI test server only. Never imported by the application entry point.
import { serve } from '@hono/node-server';
import { randomUUID } from 'node:crypto';
import { createApp } from '../build/server/app.js';
const origin='http://127.0.0.1:8885';
const {app,auth,db}=await createApp({baseURL:origin,secret:randomUUID()+randomUUID(),databasePath:'.runtime/ui-test-'+randomUUID()+'.sqlite'},{testPassword:true});
app.get('/test-login',async c=>{
  const response=await auth.handler(new Request(origin+'/api/auth/sign-up/email',{method:'POST',headers:{'Content-Type':'application/json',Origin:origin},body:JSON.stringify({name:'QA learner',email:'qa-'+randomUUID()+'@example.test',password:randomUUID()})}));
  if(!response.ok)return response;
  const headers=new Headers({Location:'/'});for(const cookie of response.headers.getSetCookie())headers.append('Set-Cookie',cookie);
  return new Response(null,{status:302,headers});
});
const server=serve({fetch:app.fetch,hostname:'127.0.0.1',port:8885});
process.on('SIGINT',()=>{server.close();db.close();process.exit();});
console.log('UI test only: '+origin+'/test-login');