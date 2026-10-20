import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('all learning tracks expose complete briefs and blank editors without answers',()=>{
  const modules=JSON.parse(readFileSync('.generated/course.json','utf8'));
  const privateTasks=JSON.parse(readFileSync('.generated/tasks.json','utf8'));
  const tasks=modules.flatMap(m=>m.tasks);
  assert.equal(tasks.length,209);
  assert.equal(new Set(tasks.map(t=>t.id)).size,tasks.length);
  const counts={};
  for(const module of modules){
    counts[module.track]=(counts[module.track]||0)+module.tasks.length;
    assert.ok(module.reference.length);
    for(const task of module.tasks){
      assert.ok(privateTasks[task.id],task.id);
      assert.equal(task.starter,'',task.id);
      assert.ok(Object.values(task.editor_files).every(code=>code===''),task.id);
      for(const key of ['solution','solution_files','setup','explanation'])assert.ok(!(key in task),`${task.id}: ${key}`);
      assert.ok(task.goal.length>=2 && task.submission_note && task.hints.length===3,task.id);
      assert.ok(task.goal.every(text=>text.split('`').length%2===1),`${task.id}: unpaired code formatting`);
      assert.ok(task.checks.every(label=>typeof label==='string'),task.id);
      for(const id of task.review||[])assert.ok(privateTasks[id],`${task.id}: missing prerequisite ${id}`);
    }
  }
  assert.deepEqual(counts,{foundations:118,intermediate:55,advanced:12,analytics:24});
  const added=modules.filter(m=>['advanced','analytics'].includes(m.track));
  assert.equal(added.length,6);
  assert.ok(added.every(m=>m.tasks.length===6 && m.tasks.at(-1).kind==='project'));
  assert.ok(added.flatMap(m=>m.tasks).every(t=>t.checks.length>=2));
});
