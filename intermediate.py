"""Intermediate learning path: original lessons with executable acceptance checks."""
from textwrap import dedent


def code(text):
    return dedent(text).strip() + '\n'


def extend_intermediate(module, task):
    def section(id, title, description, project, reference):
        m = module(id, title, description, project)
        m['track'] = 'intermediate'
        m['reference'] = reference
        return m

    def unit(m, slug, title, concept, example, goals, starter, solution, checks, hints,
             explanation, *, kind='lesson', minutes=15, review=None, files=None, setup='',
             exports=None, editors=None, solutions=None, web=False, notes=None):
        task(m, slug, title, concept, code(example), goals, code(starter), code(solution),
             [(label, code(test)) for label, test in checks], hints, explanation,
             kind=kind, minutes=minutes, files=files)
        t = m['tasks'][-1]
        t.update(time_limit=20, review=review or [], setup=code(setup) if setup else '',
                 exports=exports or [], editor_files={k: code(v) for k,v in (editors or {}).items()},
                 solution_files={k: code(v) for k,v in (solutions or {}).items()}, web_preview=web,
                 preview_path={'flask-query': 'greet', 'flask-database': 'notes'}.get(t['id'], ''))
        if notes:
            t['walkthrough'] = notes

    m = section('bridge', 'Mixed review', 'Use familiar tools in unfamiliar situations.', 'Independent readiness checks', [
        ('Work from a contract', 'def transform(records):\n    # Validate, transform, then return.\n    pass', 'Identify the expected input, output, invalid cases, and ordering rules before coding. These exercises mix previous topics and provide fewer starting lines.'),
        ('Practise recall', 'print(result)', 'Try recalling the pattern before opening hints. The Recall links revisit relevant foundation lessons. A completed exercise remains available for another attempt.')])
    unit(m,'refunds','Review · reconcile refunds',
        'A sales total can include refunds as negative amounts. You need a clean list and an audit of rejected records. Reuse conversion, validation, and functions, but apply a different input rule: blank strings and invalid decimal text are rejected; zero and negative values are legitimate. This is a readiness check, so start with the contract rather than a template.',
        'valid = [10.0, -2.0, 0.0]\nprint(sum(valid))  # 8.0',
        ['Write `reconcile(texts)`, returning `{"total": ..., "accepted": ..., "rejected": ...}`.', 'Accept finite decimal numbers only. Reject blanks, invalid text, `NaN` and infinity. Round `total` to two decimals.'],
        'def reconcile(texts):\n    pass',
        '''
        import math
        def reconcile(texts):
            values = []
            rejected = 0
            for text in texts:
                try:
                    value = float(text)
                    if not math.isfinite(value):
                        raise ValueError('nonfinite')
                    values.append(value)
                except ValueError:
                    rejected += 1
            return {'total': round(sum(values), 2), 'accepted': len(values), 'rejected': rejected}
        ''',
        [('Retain refunds and zeros', "assert reconcile(['12.50', '-2.5', '0', '', 'oops']) == {'total':10.0,'accepted':3,'rejected':2}"),
         ('Reject nonfinite values', "assert reconcile(['nan','inf','-inf']) == {'total':0,'accepted':0,'rejected':3}"),
         ('Handle an empty input', "assert reconcile([]) == {'total':0,'accepted':0,'rejected':0}")],
        ['Convert each input independently inside try/except.', 'math.isfinite(value) excludes NaN and infinity.', 'Keep accepted values and a separate rejection count.'],
        'Input validation protects the meaning of the total. A refund is real data; an unparseable amount is a data-quality problem.',
        kind='checkpoint', review=['functions-validation','analysis-missing'], minutes=20)
    unit(m,'latest','Review · retain the newest record',
        'A contact export can contain several versions of one customer. The last row in a file is not necessarily the latest update. Compare timestamps explicitly. These timestamps use the same ISO date format, so their strings sort chronologically. Preserve first-seen customer order in the output, but retain each customer’s latest record. For equal dates, retain the first record.',
        'print("2026-03-02" > "2026-02-28")  # True',
        ['Write `latest_customers(rows)`. Each row has `id`, `updated`, and `name`.', 'Keep the newest `updated` value per `id`. Return records in first-seen `id` order without mutating input.'],
        'def latest_customers(rows):\n    pass',
        '''
        def latest_customers(rows):
            latest = {}
            for row in rows:
                key = row['id']
                if key not in latest or row['updated'] > latest[key]['updated']:
                    latest[key] = row.copy()
            return list(latest.values())
        ''',
        [('Use dates rather than file position', "rows=[{'id':1,'updated':'2026-02-01','name':'new'},{'id':2,'updated':'2026-01-01','name':'B'},{'id':1,'updated':'2026-01-01','name':'old'}]\nassert latest_customers(rows)==rows[:2]"),
         ('Respect ties and empty data', "assert latest_customers([])==[]\nassert latest_customers([{'id':1,'updated':'2026-01-01','name':'A'},{'id':1,'updated':'2026-01-01','name':'B'}])[0]['name']=='A'")],
        ['Use a dictionary keyed by id.', 'Replace a stored record only for a strictly newer date.', 'Dictionary insertion order retains the first-seen id order.'],
        'You separated uniqueness, recency, and presentation order: three rules that are often accidentally combined.', kind='checkpoint',review=['collections-dicts','pandas-deduplicate'],minutes=20)
    unit(m,'quality','Review · report missing categories',
        'A regional report should account for incomplete records. Rows with missing regions cannot be assigned confidently to a group, while a zero amount is valid. Build a grouped total and an excluded count. Normalise region labels before grouping and return the result in alphabetical key order so repeated reports are predictable.',
        'totals = {}\ntotals["north"] = totals.get("north", 0) + 10',
        ['Write `region_report(rows)`, ignoring `rows` with a `None` value for `amount` or a blank stripped `region`.', 'Lowercase `region` labels. Return a dictionary with `totals` (a dictionary whose keys are alphabetically sorted) and `excluded` (the exclusion count).'],
        'def region_report(rows):\n    pass',
        '''
        def region_report(rows):
            totals = {}
            excluded = 0
            for row in rows:
                region = row['region'].strip().lower()
                if not region or row['amount'] is None:
                    excluded += 1
                    continue
                totals[region] = totals.get(region, 0) + row['amount']
            return {'totals': dict(sorted(totals.items())), 'excluded': excluded}
        ''',
        [('Group cleaned labels and keep zeros', "r=region_report([{'region':' North ','amount':10},{'region':'NORTH','amount':5},{'region':'South','amount':0},{'region':' ','amount':9},{'region':'West','amount':None}])\nassert r=={'totals':{'north':15,'south':0},'excluded':2}"),
         ('Order keys and handle empty input', "assert list(region_report([{'region':'Z','amount':1},{'region':'A','amount':2}])['totals'])==['a','z']\nassert region_report([])=={'totals':{},'excluded':0}")],
        ['Clean the region before deciding whether it is missing.', 'Use is None rather than truthiness for amounts.', 'Sort totals.items() before constructing the output dictionary.'],
        'The report explains both retained measurements and excluded records.',kind='checkpoint',review=['collections-frequency','analysis-group-means'],minutes=20)
    unit(m,'contract','Review · test an unseen input',
        'A function that works on one example may still fail at a boundary. Write a small acceptance function that checks another function supplied to it. This introduces testing as executable reasoning: your checks should distinguish a correct implementation from plausible bugs. The function under test computes shipping: zero for orders of at least 50, otherwise 4.',
        'def accepts(candidate):\n    return candidate(50) == 0',
        ['Write `accepts_shipping(candidate)`, returning `True` only if `candidate` passes inputs 0, 49, 50, and 80.', 'Expected outputs are 4, 4, 0, 0. If `candidate` raises an exception, return `False`.'],
        'def accepts_shipping(candidate):\n    pass',
        '''
        def accepts_shipping(candidate):
            try:
                return all(candidate(value) == expected for value, expected in [(0,4),(49,4),(50,0),(80,0)])
            except Exception:
                return False
        ''',
        [('Accept correct behavior', 'assert accepts_shipping(lambda x: 0 if x >= 50 else 4) is True'),
         ('Catch boundary and constant-output bugs', 'assert accepts_shipping(lambda x: 0 if x > 50 else 4) is False\nassert accepts_shipping(lambda x: 0) is False'),
         ('Handle an exception', 'def broken(x):\n    raise ValueError()\nassert accepts_shipping(broken) is False')],
        ['Store input/expected-output pairs.', 'Call the candidate for each pair.', 'Catch exceptions around the test calls.'],
        'Boundary cases reveal errors that a mid-range example misses. You will build on this in the testing module.',kind='checkpoint',review=['flow-boundary','functions-return'],minutes=20)

    m = section('arrays','NumPy for analysis','Calculate with arrays, shapes, and masks.','Analyse sensor readings',[
        ('Arrays and vector operations','values = np.array([1, 2, 3], dtype=float)\nscaled = values * 10','An array has a shape and a dtype. Arithmetic acts elementwise; Python lists have different multiplication behavior.'),
        ('Axes and masks','column_means = matrix.mean(axis=0)\nselected = values[values > 0]','axis=0 reduces rows and leaves one result per column. Boolean masks select matching positions.'),
        ('Missing and finite values','valid = values[np.isfinite(values)]','NaN is not equal to itself. Use np.isnan or np.isfinite instead of equality comparisons.')])
    unit(m,'vector','Calculate with a whole array',
        'NumPy arrays store numerical data in a uniform structure. Multiplication acts on every element, unlike list multiplication, which repeats the list. Convert input once, then express the calculation directly. Keep results as arrays until you need an ordinary list for display or serialization. This is the foundation of vectorised analysis.',
        'import numpy as np\nx = np.array([2, 4, 6])\nprint(x * 3)  # [6 12 18]',
        ['Convert `celsius` to a float array called `temperatures`.', 'Create `fahrenheit` with `temperatures * 9 / 5 + 32`.'],
        'import numpy as np\ncelsius = [0, 20, 37, -10]',
        'import numpy as np\ncelsius = [0, 20, 37, -10]\ntemperatures = np.array(celsius, dtype=float)\nfahrenheit = temperatures * 9 / 5 + 32',
        [('Create a numeric array','assert isinstance(temperatures, np.ndarray) and temperatures.dtype.kind == "f"'),('Convert all readings','assert np.allclose(fahrenheit,[32,68,98.6,14])')],
        ['Use np.array(..., dtype=float).','Write the formula once using the entire array.','np.allclose compares floating-point arrays approximately.'],
        'Vector operations express what happens to every observation without a Python loop.',review=['basics-types'],notes=['The list becomes an array.','Multiplication acts at each position.','The result retains the same shape.'])
    unit(m,'shape','Read a two-dimensional array',
        'A two-dimensional array has rows and columns. shape reports both dimensions. Index with matrix[row, column], and use : to select a complete row or column. Before summarising a matrix, identify what each dimension represents. Here rows are days and columns are sensor locations.',
        'matrix = np.array([[1, 2], [3, 4]])\nprint(matrix[:, 0])  # [1 3]',
        ['Set `shape` to `readings.shape`.', 'Set `second_day` to row index 1 and `first_sensor` to column index 0.'],
        'import numpy as np\nreadings = np.array([[10,20],[12,18],[14,16]])',
        'import numpy as np\nreadings = np.array([[10,20],[12,18],[14,16]])\nshape = readings.shape\nsecond_day = readings[1, :]\nfirst_sensor = readings[:, 0]',
        [('Understand dimensions','assert shape == (3,2)'),('Select row and column','assert second_day.tolist()==[12,18] and first_sensor.tolist()==[10,12,14]')],
        ['shape is a tuple.','Use readings[1, :].','Use readings[:, 0].'],
        'A column selects one sensor across days; a row selects all sensors on one day.',review=['collections-slices'])
    unit(m,'axes','Summarise along the right axis',
        'An aggregation reduces one or more dimensions. mean(axis=0) combines rows and returns one mean per column. mean(axis=1) combines columns and returns one mean per row. A mean without axis reduces the entire array. Write the intended question in words before choosing the axis.',
        'matrix = np.array([[2,4],[6,8]])\nprint(matrix.mean(axis=0))  # [4. 6.]',
        ['Compute `per_sensor` means, `per_day` means, and `overall` from `readings`.'],
        'import numpy as np\nreadings = np.array([[10,20],[12,18],[14,16]])',
        'import numpy as np\nreadings = np.array([[10,20],[12,18],[14,16]])\nper_sensor=readings.mean(axis=0)\nper_day=readings.mean(axis=1)\noverall=readings.mean()',
        [('Reduce rows for sensor summaries','assert np.allclose(per_sensor,[12,18])'),('Reduce columns for daily summaries','assert np.allclose(per_day,[15,15,15]) and overall==15')],
        ['Rows represent days.','Reduce rows with axis=0 to summarise sensors.','Use axis=1 for per-day means.'],
        'The output shape is a useful check that you reduced the intended dimension.',review=['analysis-group-means'])
    unit(m,'masks','Filter finite readings',
        'A Boolean mask has one truth value per observation. Combine masks with & and parenthesise each comparison. np.isfinite excludes NaN and both infinities. Missing-value filtering should preserve valid zero observations. The filtered array can be shorter than its input, which is why an audit count is useful.',
        'valid = values[np.isfinite(values) & (values >= 0)]',
        ['Create `cleaned` with finite, nonnegative `values` only.', 'Set `rejected` to the number of removed readings.'],
        'import numpy as np\nvalues=np.array([0,12,np.nan,-2,np.inf,8])',
        'import numpy as np\nvalues=np.array([0,12,np.nan,-2,np.inf,8])\ncleaned=values[np.isfinite(values) & (values>=0)]\nrejected=values.size-cleaned.size',
        [('Preserve zero and valid readings','assert cleaned.tolist()==[0,12,8]'),('Count removed values','assert rejected==3')],
        ['Use np.isfinite(values).','Combine it with values >= 0 using &.','Compare the array sizes.'],
        'Masking makes the exclusion rule explicit and retains the accepted observation order.',review=['analysis-missing'])
    unit(m,'broadcast','Scale each column differently',
        'Broadcasting allows operations between compatible shapes. A one-dimensional array with one value per column can scale every row of a matrix. NumPy aligns dimensions from the right, so the scale vector here must match the number of columns. Inspect the shape before applying a rule across a table.',
        'matrix = np.array([[1,2],[3,4]])\nprint(matrix * np.array([10,100]))',
        ['Create `converted` by multiplying each `units` column by its corresponding `prices` value.', 'Create `daily_total` by summing each `converted` row.'],
        'import numpy as np\nunits=np.array([[2,1],[3,4],[0,2]])\nprices=np.array([5,8])',
        'import numpy as np\nunits=np.array([[2,1],[3,4],[0,2]])\nprices=np.array([5,8])\nconverted=units*prices\ndaily_total=converted.sum(axis=1)',
        [('Scale by column','assert converted.tolist()==[[10,8],[15,32],[0,16]]'),('Summarise each row','assert daily_total.tolist()==[18,47,16]')],
        ['prices has one entry for each product column.','Multiply units by prices directly.','Sum across columns with axis=1.'],
        'Broadcasting avoids manually repeating the price vector for every day.',review=['collections-items'])
    unit(m,'sensor-project','Project · audit a sensor feed',
        'Combine array construction, validation, and statistics in a reusable function. The feed contains missing and impossible measurements. Keep only finite readings between 0 and 100 inclusive. Report the valid count, rejected count, mean, and maximum. No accepted observations should produce None for the two statistics.',
        'mask = np.isfinite(values) & (values >= 0) & (values <= 100)',
        ['Write `sensor_report(readings)` returning `count`, `rejected`, `mean`, `maximum`.', 'Round `mean` to two decimals and handle empty/all-invalid feeds.'],
        'import numpy as np\n\ndef sensor_report(readings):\n    pass',
        '''
        import numpy as np
        def sensor_report(readings):
            values=np.array(readings,dtype=float)
            clean=values[np.isfinite(values)&(values>=0)&(values<=100)]
            return {'count':int(clean.size),'rejected':int(values.size-clean.size),'mean':round(float(clean.mean()),2) if clean.size else None,'maximum':float(clean.max()) if clean.size else None}
        ''',
        [('Audit mixed readings',"assert sensor_report([0,20,100,float('nan'),101,-1])=={'count':3,'rejected':3,'mean':40.0,'maximum':100.0}"),('Handle no valid readings',"assert sensor_report([])=={'count':0,'rejected':0,'mean':None,'maximum':None}\nassert sensor_report([float('inf')])['count']==0")],
        ['Construct a float array and a three-part mask.','Use clean.size to detect an empty result.','Convert NumPy scalars into ordinary numbers for the returned report.'],
        'The function combines measurements with an explicit quality audit. Try a different feed after passing the checks.',kind='project',minutes=25,review=['bridge-refunds','analysis-audit-review'])

    m = section('charts','Charts that explain data','Create, inspect, and export Matplotlib figures.','Make a small sales dashboard',[
        ('Figure and axes','fig, ax = plt.subplots()\nax.plot(x, y)\nax.set(title="Trend", xlabel="Day", ylabel="Revenue")','The figure is the whole canvas; an axes object is a plotting area. Codey captures open figures after a run and displays them under Output files.'),
        ('Choose a chart','ax.bar(labels, values)\nax.hist(values, bins=[0,10,20,30])\nax.scatter(x,y)','Lines show ordered change, bars compare categories, histograms show distributions, and scatter plots compare paired measurements.'),
        ('Save for sharing','fig.tight_layout()\nfig.savefig("chart.png", dpi=150)','Label units, use informative titles, and keep bar-chart baselines at zero. Download declared outputs from the Output files tab.')])
    unit(m,'line','Plot a trend with labelled axes',
        'A line chart connects observations in a meaningful order, such as time. Create a figure and axes, then draw through the axes object. Labels should tell the reader what is measured and in what units. Codey automatically displays open Matplotlib figures after Run; you do not need an interactive desktop plotting window.',
        'import matplotlib.pyplot as plt\nfig, ax = plt.subplots()\nax.plot([1,2,3], [10,15,12], marker="o")\nax.set(xlabel="Day", ylabel="Orders", title="Daily orders")',
        ['Plot `days` against `revenue` on an axes named `ax`, with a figure named `fig`.', 'Use `title` `"Weekly revenue"`, `xlabel` `"Day"`, and `ylabel` `"Revenue"`.'],
        'import matplotlib.pyplot as plt\ndays=[1,2,3,4,5]\nrevenue=[20,35,30,45,50]',
        'import matplotlib.pyplot as plt\ndays=[1,2,3,4,5]\nrevenue=[20,35,30,45,50]\nfig,ax=plt.subplots()\nax.plot(days,revenue,marker="o")\nax.set(title="Weekly revenue",xlabel="Day",ylabel="Revenue")\nfig.tight_layout()',
        [('Plot the correct data','assert len(ax.lines)==1 and list(ax.lines[0].get_ydata())==[20,35,30,45,50] and list(ax.lines[0].get_xdata())==[1,2,3,4,5]'),('Label the chart','assert ax.get_title()=="Weekly revenue" and ax.get_xlabel()=="Day" and ax.get_ylabel()=="Revenue"')],
        ['Create fig, ax with plt.subplots().','Call ax.plot(days, revenue).','Use ax.set with the three requested labels.'],
        'The rise and dip are visible, and the labels make the measurements understandable outside the code.',review=['analysis-growth'])
    unit(m,'bar','Compare categories honestly',
        'A bar chart uses length to encode magnitude, so its numeric baseline should normally begin at zero. Sort categories by value when the ranking is the story. Keep labels aligned with the reordered values; sorting one without the other creates a misleading chart. Here horizontal bars leave room for product names.',
        'ax.barh(["Tea", "Cake"], [20,12])\nax.set_xlim(left=0)',
        ['Draw a horizontal bar chart in `ax` with Coffee, Tea, Cake and revenues 40, 30, 12.', 'Set `xlabel` to `"Revenue"` and `title` to `"Revenue by product"`. Start the x axis at zero.'],
        'import matplotlib.pyplot as plt\nproducts=["Coffee","Tea","Cake"]\nrevenue=[40,30,12]',
        'import matplotlib.pyplot as plt\nproducts=["Coffee","Tea","Cake"]\nrevenue=[40,30,12]\nfig,ax=plt.subplots()\nax.barh(products,revenue)\nax.set(title="Revenue by product",xlabel="Revenue")\nax.set_xlim(left=0)\nfig.tight_layout()',
        [('Compare the intended values','assert [p.get_width() for p in ax.patches]==[40,30,12]'),('Label categories and start at zero','assert [t.get_text() for t in ax.get_yticklabels()]==["Coffee","Tea","Cake"] and ax.get_xlim()[0]==0 and ax.get_xlabel()=="Revenue" and ax.get_title()=="Revenue by product"')],
        ['Use barh for horizontal bars.','Pass matching labels and values.','Set the left x-limit to zero.'],
        'The baseline and labels preserve the meaning of each bar’s length.',review=['analysis-rank-ties'])
    unit(m,'histogram','Show a distribution',
        'A histogram groups numeric observations into intervals and counts them. Its appearance depends on the bin boundaries, so choose and report them deliberately. Adjacent bins represent neighbouring ranges rather than unrelated categories. NumPy-style histogram bins include the left edge and exclude the right, except that the final bin includes its right edge.',
        'counts, edges, patches = ax.hist(values, bins=[0,10,20,30])',
        ['Plot `minutes` into bins `[0,10,20,30]`, storing `counts` and `edges` from `ax.hist`.', 'Label x `"Minutes"` and y `"Deliveries"`.'],
        'import matplotlib.pyplot as plt\nminutes=[2,5,9,10,12,19,20,25,30]',
        'import matplotlib.pyplot as plt\nminutes=[2,5,9,10,12,19,20,25,30]\nfig,ax=plt.subplots()\ncounts,edges,patches=ax.hist(minutes,bins=[0,10,20,30])\nax.set(xlabel="Minutes",ylabel="Deliveries",title="Delivery times")',
        [('Use the requested bins','assert list(edges)==[0,10,20,30] and list(counts)==[3,3,3]'),('Draw and label the distribution','assert len(ax.patches)==3 and ax.get_xlabel()=="Minutes" and ax.get_ylabel()=="Deliveries"')],
        ['Pass explicit bin edges.','Unpack the three returned values.','30 belongs to the final bin.'],
        'Explicit bin edges make the calculation reproducible. Try narrower bins and observe how the same data tells a more detailed story.',review=['flow-boundary','analysis-statistics'])
    unit(m,'scatter','Compare paired measurements',
        'A scatter plot keeps each x measurement paired with its corresponding y measurement. It can reveal patterns and unusual points without assuming that x caused y. Reordering one series independently breaks those pairs. Here compare advertising spend with revenue and compute correlation as a description, not a causal claim.',
        'ax.scatter(spend, revenue)\ncorrelation = np.corrcoef(spend, revenue)[0,1]',
        ['Scatter `spend` against `revenue` in `ax` and calculate `correlation`.', 'Use `xlabel` `"Ad spend"` and `ylabel` `"Revenue"`.'],
        'import numpy as np\nimport matplotlib.pyplot as plt\nspend=[10,20,30,40]\nrevenue=[25,40,35,60]',
        'import numpy as np\nimport matplotlib.pyplot as plt\nspend=[10,20,30,40]\nrevenue=[25,40,35,60]\nfig,ax=plt.subplots()\nax.scatter(spend,revenue)\nax.set(xlabel="Ad spend",ylabel="Revenue",title="Spend and revenue")\ncorrelation=float(np.corrcoef(spend,revenue)[0,1])',
        [('Preserve the paired points','assert np.allclose(ax.collections[0].get_offsets(),[[10,25],[20,40],[30,35],[40,60]])'),('Calculate and label the comparison','assert abs(correlation-float(np.corrcoef(spend,revenue)[0,1]))<1e-8 and ax.get_xlabel()=="Ad spend" and ax.get_ylabel()=="Revenue"')],
        ['Use scatter rather than plot.','np.corrcoef returns a matrix; select [0,1].','Preserve the original order of both lists.'],
        'The relationship is positive in this small sample, but these four observations do not establish cause and effect.',review=['arrays-vector','analysis-spread'])
    unit(m,'export','Export a chart you can share',
        'A saved chart should make sense without the notebook or lesson beside it. Add a title, axis labels, and a sensible layout before exporting. PNG is a bitmap format convenient for sharing. The export happens before the practice folder is removed, and Codey lets you download the declared file from Output files.',
        'fig.tight_layout()\nfig.savefig("report.png", dpi=150)',
        ['Create a vertical bar chart for `North=30` and `South=20` in `ax`.', 'Title it `"Regional sales"`, label the y axis `"Revenue"`, and save `report.png`.'],
        'import matplotlib.pyplot as plt',
        'import matplotlib.pyplot as plt\nfig,ax=plt.subplots()\nax.bar(["North","South"],[30,20])\nax.set(title="Regional sales",ylabel="Revenue")\nfig.tight_layout()\nfig.savefig("report.png",dpi=150)',
        [('Create the labelled bars','assert [p.get_height() for p in ax.patches]==[30,20] and ax.get_title()=="Regional sales" and ax.get_ylabel()=="Revenue"'),('Save an actual PNG','from pathlib import Path\nassert Path("report.png").read_bytes().startswith(bytes([137,80,78,71]))')],
        ['Build the chart before saving.','Call tight_layout to reduce clipping.','Use fig.savefig("report.png", dpi=150).'],
        'The download preserves the chart after the attempt finishes. Inspect the image, not only its filename.',exports=['report.png'])
    unit(m,'dashboard','Project · two views of the same sales',
        'A useful report can show both change over time and contribution by category. Build one figure with two plotting areas, using one dataset for each question. Keep titles and labels specific. This project gives an output contract rather than a completed plotting template; use the reference and earlier examples as needed.',
        'fig, axes = plt.subplots(1, 2, figsize=(10,4))\nleft, right = axes',
        ['Create `fig` with two axes named `trend` and `categories`.', 'Plot `daily = [10,20,15,30]` against days 1–4 on `trend`; title `"Daily revenue"`.', 'Plot `Tea=40` and `Cake=35` as bars on `categories`; title `"Product revenue"`. Label both y axes `"Revenue"` and save `dashboard.png`.'],
        'import matplotlib.pyplot as plt\ndaily=[10,20,15,30]',
        'import matplotlib.pyplot as plt\ndaily=[10,20,15,30]\nfig,(trend,categories)=plt.subplots(1,2,figsize=(10,4))\ntrend.plot([1,2,3,4],daily,marker="o")\ntrend.set(title="Daily revenue",xlabel="Day",ylabel="Revenue")\ncategories.bar(["Tea","Cake"],[40,35])\ncategories.set(title="Product revenue",ylabel="Revenue")\nfig.tight_layout()\nfig.savefig("dashboard.png",dpi=150)',
        [('Use two views with correct data','assert len(fig.axes)==2 and list(trend.lines[0].get_ydata())==[10,20,15,30] and [p.get_height() for p in categories.patches]==[40,35]'),('Provide interpretable titles','assert trend.get_title()=="Daily revenue" and categories.get_title()=="Product revenue" and trend.get_ylabel()==categories.get_ylabel()=="Revenue"'),('Export the dashboard','from pathlib import Path\nassert Path("dashboard.png").read_bytes().startswith(bytes([137,80,78,71]))')],
        ['Use plt.subplots(1,2).','Use a line for ordered days and bars for categories.','Label each axes separately before saving the whole figure.'],
        'The chart answers two distinct questions. Check that category totals and daily totals both reconcile to 75.',kind='project',minutes=30,exports=['dashboard.png'],review=['analysis-report-2','charts-line'])

    from intermediate_data import add_data_modules
    add_data_modules(section, unit)
    from intermediate_apps import add_app_modules
    add_app_modules(section, unit)
