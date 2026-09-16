import { betterAuth,type BetterAuthOptions } from 'better-auth';
import { getMigrations } from 'better-auth/db/migration';
import type { DatabaseSync } from 'node:sqlite';
import type { Config } from './config.js';

export async function createAuth(config:Config,db:DatabaseSync,testPassword=false){
  const options={
    appName:'Codey',baseURL:config.baseURL,secret:config.secret,database:db,
    trustedOrigins:[config.baseURL],
    socialProviders:{...(config.google?{google:config.google}:{}),...(config.github?{github:config.github}:{})},
    // Enabled only by the integration test factory, never by the server entry point.
    emailAndPassword:{enabled:testPassword},
    account:{accountLinking:{enabled:false}},
    session:{expiresIn:60*60*24*14,updateAge:60*60*24,cookieCache:{enabled:false}},
    rateLimit:{enabled:true,window:60,max:60,storage:'database'},
    advanced:{useSecureCookies:config.baseURL.startsWith('https:'),defaultCookieAttributes:{httpOnly:true,sameSite:'lax'}},
    telemetry:{enabled:false},
  } satisfies BetterAuthOptions;
  const migration=await getMigrations(options);
  await migration.runMigrations();
  return betterAuth(options);
}
