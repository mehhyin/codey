import { serve } from '@hono/node-server';
import { writeFileSync,mkdirSync,unlinkSync } from 'node:fs';
import { randomBytes,timingSafeEqual } from 'node:crypto';
import { join } from 'node:path';
import { createApp } from './app.js';
import { configFromEnvironment } from './config.js';

const config=configFromEnvironment();
const port=config.port!;
const {app,db}=await createApp(config);
const controlToken=randomBytes(32).toString('hex');
const controlDir=process.env.CODEY_CONTROL_DIR||'.runtime';
const controlPath=join(controlDir,`control-${port}.json`);
app.post('/api/shutdown',c=>{
  const supplied=Buffer.from(c.req.header('X-Codey-Control')||'');
  const expected=Buffer.from(controlToken);
  if(supplied.length!==expected.length||!timingSafeEqual(supplied,expected))return c.json({error:'Use Stop Codey.cmd.'},403);
  setTimeout(shutdown,100);return c.json({stopping:true});
});
const server=serve({fetch:app.fetch,hostname:config.host,port});
mkdirSync(controlDir,{recursive:true});writeFileSync(controlPath,JSON.stringify({url:config.baseURL,token:controlToken,pid:process.pid}),{mode:0o600});
console.log(`Codey is ready at ${config.baseURL}`);
console.log(`SQLite: ${config.databasePath}. Python runs in the browser.`);
if(!config.google&&!config.github)console.log('Add OAuth credentials to .env to enable Google/GitHub sign-in. Guest practice remains available.');
function shutdown(){server.close();db.close();try{unlinkSync(controlPath);}catch{}process.exit(0);}
for(const signal of ['SIGINT','SIGTERM'] as const)process.on(signal,shutdown);
