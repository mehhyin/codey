import { readFileSync,writeFileSync,existsSync,mkdirSync,copyFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const root='.runtime/pyodide';mkdirSync(root,{recursive:true});
const pkg=JSON.parse(readFileSync('node_modules/pyodide/package.json','utf8'));
const lock=JSON.parse(readFileSync('node_modules/pyodide/pyodide-lock.json','utf8'));
for(const name of ['pyodide.js','pyodide.mjs','pyodide.asm.mjs','pyodide.asm.wasm','python_stdlib.zip','pyodide-lock.json'])copyFileSync('node_modules/pyodide/'+name,root+'/'+name);
const needed=new Set();
function add(name){if(needed.has(name))return;const p=lock.packages[name];if(!p)throw Error('Missing Pyodide package '+name);needed.add(name);p.depends.forEach(add);}
['numpy','pandas','matplotlib','micropip','sqlite3','ssl','markupsafe'].filter(n=>lock.packages[n]).forEach(add);
// Unvendored standard-library extensions use leading underscores in some releases.
['_sqlite3','_ssl'].filter(n=>lock.packages[n]).forEach(add);
async function download(url,file,hash){
 if(existsSync(file)&&createHash('sha256').update(readFileSync(file)).digest('hex')===hash)return;
 const response=await fetch(url);if(!response.ok)throw Error(`Download failed (${response.status}): ${url}`);
 const data=Buffer.from(await response.arrayBuffer());
 if(createHash('sha256').update(data).digest('hex')!==hash)throw Error('Checksum mismatch: '+file);
 writeFileSync(file,data);console.log('Downloaded '+file.split('/').at(-1));
}
for(const name of needed){const p=lock.packages[name];await download(`https://cdn.jsdelivr.net/pyodide/v${pkg.version}/full/${p.file_name}`,`${root}/${p.file_name}`,p.sha256);}
const wheels=[];
for(const [name,version] of Object.entries({openpyxl:'3.1.5','et-xmlfile':'2.0.0',flask:'3.1.3',werkzeug:'3.1.8',jinja2:'3.1.6',click:'8.5.0',blinker:'1.9.0',itsdangerous:'2.2.0'})){
 const response=await fetch(`https://pypi.org/pypi/${name}/${version}/json`);if(!response.ok)throw Error('Cannot resolve '+name);
 const meta=await response.json();const wheel=meta.urls.find(f=>f.filename.endsWith('none-any.whl'));if(!wheel)throw Error('No portable wheel for '+name);
 await download(wheel.url,`${root}/${wheel.filename}`,wheel.digests.sha256);wheels.push(wheel.filename);
}
writeFileSync(root+'/runtime.json',JSON.stringify({version:pkg.version,packages:[...needed],wheels}));
console.log('Browser Python assets prepared locally, with verified package checksums.');
