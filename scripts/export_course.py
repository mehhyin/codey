import ast
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from course import all_tasks,public_course

target=ROOT/'.generated'
target.mkdir(exist_ok=True)
tasks=all_tasks()
for task in tasks.values():
    referenced={n.id for check in task['checks'] for n in ast.walk(ast.parse(check['code'])) if isinstance(n,ast.Name)}
    imports=[]
    for node in ast.parse(task['starter']).body:
        if isinstance(node,(ast.Import,ast.ImportFrom)) and referenced & {a.asname or a.name.split('.')[0] for a in node.names}:
            imports.append(ast.unparse(node))
    task['check_imports']='\n'.join(imports)
modules=public_course()
for module in modules:
    for task in module['tasks']:
        if 'practice_api.py' in task['files']:
            task['files']['practice_api.py']=(ROOT/'runner'/'practice_api.py').read_text(encoding='utf-8')
            task['runtime_note']='The practice API runs offline inside browser Python. Its adapter models requests, status codes, pagination and retries without opening network connections.'
        elif task.get('web_preview'):
            task['runtime_note']='Preview app runs Flask with its test client inside browser Python. Forms and links work here; learner JavaScript and external network requests are disabled. Preview data resets when you run again, switch exercises or reload.'
(target/'course.json').write_text(json.dumps(modules,ensure_ascii=False),encoding='utf-8')
(target/'tasks.json').write_text(json.dumps(tasks,ensure_ascii=False),encoding='utf-8')
print(f'Exported {len(tasks)} exercises; existing IDs and question formatting preserved.')
