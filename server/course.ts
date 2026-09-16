import { readFileSync } from 'node:fs';
export type Task={id:string;goal:string[];hints:string[];solution:string;solution_files?:Record<string,string>;
  files:Record<string,string>;editor_files?:Record<string,string>;checks:{label:string;code:string}[];
  setup?:string;check_imports?:string;explanation:string;exports?:string[];time_limit?:number;web_preview?:boolean;preview_path?:string};
export const modules=JSON.parse(readFileSync('.generated/course.json','utf8'));
export const tasks:Record<string,Task>=Object.assign(Object.create(null),JSON.parse(readFileSync('.generated/tasks.json','utf8')));
