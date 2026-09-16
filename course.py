"""Editable, executable course content. Each task includes independent behavior checks."""
import ast

MODULES = []


def module(id, title, description, project):
    item = dict(id=id, title=title, description=description, project=project, tasks=[])
    MODULES.append(item)
    return item


def task(m, slug, title, concept, example, goal, starter, solution, checks, hints,
         explanation, kind='lesson', minutes=8, files=None):
    m['tasks'].append(dict(id=m['id'] + '-' + slug, title=title, concept=concept,
        example=example, goal=goal, starter=starter, solution=solution,
        checks=[dict(label=label, code=code) for label, code in checks], hints=hints,
        explanation=explanation, kind=kind, minutes=minutes, files=files or {}))


m = module('basics', 'Python essentials', 'Turn values into useful little programs.', 'Build a trip budget')
task(m, 'variables', 'Give your data a name',
    'A variable gives a value a name. Use = to assign it, then use that name in calculations. Python keeps whole numbers as int and decimal numbers as float. print() shows a result in the console.',
    'coffee_price = 4.50\ncups = 2\ncoffee_total = coffee_price * cups\nprint(coffee_total)',
    ['A notebook costs 12.50. You need 4 notebooks.', 'Create `price` and `quantity` with those values.', 'Calculate `total` using your variables, then print `total`.'],
    'price = 12.50\nquantity = 4\n\n# Calculate the total, then print it.\n',
    'price = 12.50\nquantity = 4\ntotal = price * quantity\nprint(total)',
    [('Store the price and quantity', 'assert price == 12.5 and quantity == 4'), ('Calculate a total of 50', 'assert total == 50'), ('Print the total', 'assert __output__.strip() in ("50", "50.0", "50.00")')],
    ['Multiply the price of one notebook by the number of notebooks.', 'The multiplication operator in Python is *. Store the result in total.', 'Use total = price * quantity, then print(total).'],
    'The variables describe the inputs. Multiplication produces a number, and print() makes that number visible. Changing quantity and running the calculation again updates the total.')
task(m, 'strings', 'Make numbers readable',
    'Strings hold text inside quotes. An f-string starts with f before the opening quote. Expressions inside {braces} are inserted into the text. Use :.2f inside the braces to display two decimal places.',
    'name = "Coffee"\ncost = 4.5\nmessage = f"{name}: {cost:.2f}"\nprint(message)',
    ['Set `item` to `"Notebook"` and `total` to 50.', 'Create `message` with the exact text `"Notebook: 50.00"` using those values.', 'Print `message`.'],
    'item = "Notebook"\ntotal = 50\n\n# Build and print message.\n',
    'item = "Notebook"\ntotal = 50\nmessage = f"{item}: {total:.2f}"\nprint(message)',
    [('Build the receipt text', 'assert message == "Notebook: 50.00"'), ('Print the message', 'assert __output__.strip() == message')],
    ['Combine a string with your numeric value.', 'Try an f-string: f"{item}: {total:.2f}".', 'Assign the f-string to message, then call print(message).'],
    'Formatting changes how a value is displayed without changing the original number. That is useful for receipts and reports.')
task(m, 'conversion', 'Turn text into numbers',
    'Values read from forms and many files begin as text. int() converts integer text, and float() converts decimal text. Adding strings joins them; adding numbers does arithmetic.',
    'text = "8.25"\namount = float(text)\nprint(amount + 2)',
    ['Convert `price_text` to a `float` called `price`.', 'Convert `quantity_text` to an `int` called `quantity`.', 'Calculate `total`. It should equal 37.5.'],
    'price_text = "12.50"\nquantity_text = "3"\n\n# Convert before calculating.\n',
    'price_text = "12.50"\nquantity_text = "3"\nprice = float(price_text)\nquantity = int(quantity_text)\ntotal = price * quantity\nprint(total)',
    [('Convert to numeric types', 'assert isinstance(price, float) and isinstance(quantity, int)'), ('Calculate the numeric total', 'assert total == 37.5')],
    ['Both starting values are strings, even though they contain digits.', 'Use float(price_text) for the decimal and int(quantity_text) for the whole number.', 'Multiply your converted price and quantity to produce total.'],
    'Converting at the input boundary makes later calculations predictable. float is convenient here; financial software often uses decimal.Decimal for exact decimal arithmetic.')
task(m, 'trip-1', 'Trip budget · the essentials',
    'Project 1 / 3. You are planning a three-night break. First, model the cost of the essentials using named inputs. Keep values numeric until the final display.',
    'ticket = 20\nvisits = 2\nactivity_cost = ticket * visits',
    ['Create `nights = 3`, `nightly_rate = 80`, and `transport = 45`.', 'Calculate `accommodation` from `nights` and `nightly_rate`.', 'Calculate `essentials` from `accommodation` and `transport`.'],
    '# Model the essential trip costs.\n',
    'nights = 3\nnightly_rate = 80\ntransport = 45\naccommodation = nights * nightly_rate\nessentials = accommodation + transport',
    [('Accommodation costs 240', 'assert accommodation == 240'), ('Essentials cost 285', 'assert essentials == 285')],
    ['Accommodation depends on the number of nights.', 'Multiply 3 by 80, then add transport.', 'accommodation = nights * nightly_rate; essentials = accommodation + transport'],
    'Separating accommodation from essentials keeps the calculation readable and lets you inspect intermediate values.', kind='project', minutes=10)
task(m, 'trip-2', 'Trip budget · room for food',
    'Project 2 / 3. Add a daily food allowance and see what remains. Each project step starts with its own inputs, so you can revisit it independently.',
    'remaining = available - spent',
    ['The `budget` is 450 and `essentials` cost 285.', 'Set `food_per_day = 25` and `days = 4`.', 'Calculate `food_total`, `trip_total`, and `remaining`.'],
    'budget = 450\nessentials = 285\n\n# Add food and calculate the remaining budget.\n',
    'budget = 450\nessentials = 285\nfood_per_day = 25\ndays = 4\nfood_total = food_per_day * days\ntrip_total = essentials + food_total\nremaining = budget - trip_total',
    [('Food costs 100', 'assert food_total == 100'), ('Trip costs 385', 'assert trip_total == 385'), ('65 remains', 'assert remaining == 65')],
    ['Work from small calculations to the final result.', 'Multiply the daily allowance by 4, then add essentials.', 'Subtract trip_total from budget to find remaining.'],
    'Breaking a calculation into named stages makes mistakes easier to locate.', kind='project', minutes=10)
task(m, 'trip-3', 'Trip budget · your summary',
    'Project 3 / 3. Finish with a readable summary. The same pattern—read inputs, calculate, format a result—appears throughout data analysis and automation.',
    'print(f"Spent: {spent:.2f}")',
    ['Using the provided totals, create `summary` with the exact text `"Trip: 385.00 | Left: 65.00"`.', 'Print `summary`.'],
    'trip_total = 385\nremaining = 65\n\n# Write your final summary.\n',
    'trip_total = 385\nremaining = 65\nsummary = f"Trip: {trip_total:.2f} | Left: {remaining:.2f}"\nprint(summary)',
    [('Format both values', 'assert summary == "Trip: 385.00 | Left: 65.00"'), ('Display your summary', 'assert __output__.strip() == summary')],
    ['Use one f-string with two expressions.', 'Format both values with :.2f.', 'Keep the spaces and the | separator exactly as shown.'],
    'You built a small program from inputs through calculations to a useful output. Next you will make programs choose what to do.', kind='project', minutes=10)


def all_tasks():
    return {t['id']: t for m in MODULES for t in m['tasks']}


def public_course():
    return [dict(id=m['id'], title=m['title'], description=m['description'], project=m['project'], reference=m.get('reference', []), track=m.get('track', 'foundations'),
        tasks=[{k: v for k, v in t.items() if k not in ('solution', 'solution_files', 'setup', 'checks', 'explanation')} |
               {'checks': [c['label'] for c in t['checks']], **blank_workspace(t)} for t in m['tasks']]) for m in MODULES]


def blank_workspace(t):
    """Keep the editor empty while presenting essential input data in the brief."""
    inputs, helpers = [], []
    if t['kind'] != 'debug':
        for node in ast.parse(t['starter']).body:
            if isinstance(node, ast.Assign):
                # Objects such as app or a database connection are implementation,
                # not input data. Preserve literals and numerical/table constructors.
                value = node.value
                literal = isinstance(value, (ast.Constant, ast.List, ast.Tuple, ast.Set, ast.Dict, ast.UnaryOp))
                constructor = isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr in ('array', 'DataFrame')
                if literal or constructor:
                    inputs.append({'name': ', '.join(ast.unparse(target) for target in node.targets), 'value': ast.unparse(value)})
            elif isinstance(node, ast.FunctionDef) and not any(isinstance(child, ast.Pass) for child in ast.walk(node)):
                helpers.append(ast.get_source_segment(t['starter'], node))
    return dict(starter='', previous_starter=t['starter'],
        editor_files={name: '' for name in t.get('editor_files', {})},
        previous_editor_files=t.get('editor_files', {}), input_data=inputs,
        provided_helpers=helpers, debug_code=t['starter'] if t['kind']=='debug' else '')


from course_extra import extend
extend(module, task)

from course_practice import expand
expand(MODULES, task)

from intermediate import extend_intermediate
extend_intermediate(module, task)
