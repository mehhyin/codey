import { resolve } from 'node:path';
export type Config = {
  baseURL:string; databasePath:string; secret:string;
  host?:string; port?:number;
  google?:{clientId:string;clientSecret:string}; github?:{clientId:string;clientSecret:string};
};
export function configFromEnvironment(env:NodeJS.ProcessEnv=process.env):Config {
  const baseURL=env.BETTER_AUTH_URL || 'http://127.0.0.1:8765';
  function origin(value:string,name:string){
    const url=new URL(value);
    if(url.origin!==value||url.username||url.password||!(url.protocol==='https:'||(url.protocol==='http:'&&['localhost','127.0.0.1','[::1]'].includes(url.hostname))))
      throw new Error(`${name} must be an HTTPS origin (HTTP is allowed only for localhost). Do not include a path or trailing slash.`);
    return url;
  }
  const url=origin(baseURL,'BETTER_AUTH_URL');
  function port(value:string|undefined,fallback:number){const n=Number(value??fallback);if(!Number.isInteger(n)||n<1||n>65535)throw new Error('Listener ports must be between 1 and 65535.');return n;}
  const appPort=port(env.PORT,Number(url.port||8765));
  const secret=env.BETTER_AUTH_SECRET||'';
  if(secret.length<32)throw new Error('Run npm run setup to create .env with a private authentication secret.');
  function provider(name:'GOOGLE'|'GITHUB'){
    const clientId=env[`${name}_CLIENT_ID`],clientSecret=env[`${name}_CLIENT_SECRET`];
    if(Boolean(clientId)!==Boolean(clientSecret))throw new Error(`Configure both ${name} OAuth credentials or leave both blank.`);
    return clientId && clientSecret?{clientId,clientSecret}:undefined;
  }
  return {baseURL,secret,databasePath:resolve(env.DATABASE_PATH||'data/codey.sqlite'),host:env.HOST||'127.0.0.1',port:appPort,google:provider('GOOGLE'),github:provider('GITHUB')};
}
