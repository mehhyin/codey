import { mkdirSync,readFileSync,writeFileSync } from 'node:fs';
import { dirname } from 'node:path';
import { randomBytes } from 'node:crypto';
// Reuse the same secret across container replacements. Never write it to logs.
if(!process.env.BETTER_AUTH_SECRET){
  const file=process.env.CODEY_SECRET_FILE||'/data/auth-secret';
  mkdirSync(dirname(file),{recursive:true});
  try{writeFileSync(file,randomBytes(48).toString('base64url'),{flag:'wx',mode:0o600});}
  catch(error){if(error.code!=='EEXIST')throw error;}
  process.env.BETTER_AUTH_SECRET=readFileSync(file,'utf8').trim();
}
if(process.argv[2]==='backup')await import('../build/server/backup.js');
else await import('../build/server/index.js');
