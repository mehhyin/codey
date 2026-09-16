import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { randomBytes } from 'node:crypto';
if (!existsSync('.env')) {
  const template=readFileSync('.env.example','utf8').replace('BETTER_AUTH_SECRET=','BETTER_AUTH_SECRET='+randomBytes(48).toString('base64url'));
  writeFileSync('.env',template,{mode:0o600});
  console.log('Created .env with a private random authentication secret. Add OAuth credentials there when ready.');
} else console.log('Existing .env preserved.');
mkdirSync('data',{recursive:true});
