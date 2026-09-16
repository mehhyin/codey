"""HTTP, software engineering, local web apps, and independent projects."""
from pathlib import Path


def add_app_modules(section, unit):
    fixture = {'practice_api.py': Path(__file__).with_name('practice_api.py').read_text(encoding='utf-8')}
    http = 'import json\nfrom urllib.request import urlopen\nfrom urllib.error import HTTPError\nfrom practice_api import base_url\n'
    fetch = '''
def fetch_json(url):
    with urlopen(url, timeout=3) as response:
        return json.load(response)
'''
    m = section('apis', 'Working with APIs', 'Make real HTTP requests to an offline practice service.', 'Download a paginated report', [
        ('Request and decode', 'from practice_api import base_url\nwith urlopen(url, timeout=3) as response:\n    data = json.load(response)', 'HTTP transfers bytes; JSON decoding creates Python lists and dictionaries. Our practice service runs on your computer, with no account or internet required.'),
        ('Query parameters', 'url = base_url + "/search?" + urlencode({"q": "tea & cake"})', 'Encode values instead of manually replacing spaces. Status codes describe success and failure.'),
        ('Resilient clients', 'for attempt in range(3):\n    # Retry temporary failures only.\n    pass', 'Always set a timeout and bound retries. Follow pagination until the response has no next page.')])
    unit(m,'get','Decode an HTTP response','An API returns structured data over HTTP. Open a response inside a with block so the connection closes. json.load reads the response and decodes its JSON. The fixture starts a tiny local server; base_url contains its address. This behaves like an HTTP API without requiring an online account.',http+fetch,['Define fetch_json(url) and assign status from /status.'],http+'\n# Define your function here',http+fetch+'\nstatus=fetch_json(base_url+"/status")', [('Read server data','assert status=={"ok":True}\nassert fetch_json(base_url+"/status")["ok"] is True')],['Use urlopen with timeout=3.','Pass the response to json.load.','Append /status to base_url.'],'The response body is now an ordinary dictionary.',files=fixture,review=['files-json'])
    unit(m,'query','Encode a search query','A query can contain spaces, ampersands, or non-English text. These characters must be encoded so they remain part of a value instead of changing the URL structure. urllib.parse.urlencode builds a query string from a dictionary. The practice endpoint echoes the query so you can verify that it survives the round trip.', 'from urllib.parse import urlencode\nprint(urlencode({"q":"tea & cake"}))',['Write search(text), returning the query value echoed by /search.'],http+fetch+'\ndef search(text):\n    pass',http+fetch+'\nfrom urllib.parse import urlencode\ndef search(text):\n    return fetch_json(base_url+"/search?"+urlencode({"q":text}))["query"]',[('Preserve punctuation and Unicode','assert search("tea & cake")=="tea & cake"\nassert search("café + 2")=="café + 2"'),('Accept an empty query','assert search("")==""')],['Import urlencode.','Encode a dictionary with key q.','Read the query field from the response.'],'Encoding preserves the meaning of user input.',files=fixture,review=['web-query'])
    unit(m,'errors','Handle a missing resource','urlopen raises HTTPError for an unsuccessful HTTP status. Decide which errors your function can handle meaningfully. Here a missing resource is an expected result, so return None for 404. Re-raise other HTTP errors so a server outage does not silently look like missing data.', 'try:\n    data = fetch_json(url)\nexcept HTTPError as error:\n    print(error.code)',['Define optional_json(url): return decoded JSON on success, None on 404, and re-raise other HTTPError values.'],http+fetch+'\ndef optional_json(url):\n    pass',http+fetch+'\ndef optional_json(url):\n    try:\n        return fetch_json(url)\n    except HTTPError as error:\n        if error.code == 404:\n            return None\n        raise',[('Handle success and missing data','assert optional_json(base_url+"/status")=={"ok":True}\nassert optional_json(base_url+"/missing") is None'),('Keep other failures visible','from unittest.mock import patch\nwith patch.dict(optional_json.__globals__, {"fetch_json":lambda url: (_ for _ in ()).throw(HTTPError(url,500,"error",{},None))}):\n    try:\n        optional_json(base_url)\n    except HTTPError as e:\n        assert e.code==500\n    else:\n        assert False')],['Catch HTTPError, not every exception.','Inspect error.code.','Use bare raise for unexpected errors.'],'An expected absence and a failed service have different meanings.',files=fixture,review=['functions-validation'])
    pages = '''
def all_orders():
    items=[]
    path='/orders?page=1'
    while path:
        page=fetch_json(base_url+path)
        items.extend(page['items'])
        path=page['next']
    return items
'''
    unit(m,'pages','Follow pagination','Many APIs split a collection across pages. Reading only the first response gives an incomplete report. This service returns items and a next path. Append the items, request the next path, and stop at None. The practice service uses only local relative paths and a finite page sequence.',http+fetch,['Define all_orders(), returning all records in page order.'],http+fetch+'\ndef all_orders():\n    pass',http+fetch+pages,[('Collect every page','assert all_orders()==[{"id":1,"amount":10},{"id":2,"amount":20},{"id":3,"amount":5}]')],['Start at /orders?page=1.','Extend one list with page["items"].','Replace the path with page["next"].'],'Pagination is part of data completeness, not just connection handling.',files=fixture,review=['flow-while'])
    unit(m,'retry','Retry temporary failures within a limit','A temporary server failure may succeed on another attempt. A missing resource usually will not. Implement a bounded retry policy: retry HTTP 503 up to attempts calls, then raise the final error. This exercise omits delays to keep feedback fast; a production client would also use backoff and honour server retry instructions.', 'for attempt in range(attempts):\n    print(attempt)',['Write retry_json(url, attempts=3). Retry only HTTP 503; immediately raise other errors.', 'Require attempts >= 1, otherwise raise ValueError.'],http+fetch+'\ndef retry_json(url, attempts=3):\n    pass',http+fetch+'''
def retry_json(url, attempts=3):
    if attempts < 1:
        raise ValueError('attempts must be positive')
    for attempt in range(attempts):
        try:
            return fetch_json(url)
        except HTTPError as error:
            if error.code != 503 or attempt == attempts-1:
                raise
''',[('Recover from a temporary response','assert retry_json(base_url+"/unstable")=={"ok":True}'),('Bound retries and reject invalid limits','from unittest.mock import Mock, patch\nfor status, expected in [(503,3),(404,1)]:\n    fake=Mock(side_effect=HTTPError(base_url,status,"error",{},None))\n    with patch.dict(retry_json.__globals__, {"fetch_json":fake}):\n        try:\n            retry_json(base_url)\n        except HTTPError:\n            pass\n        else:\n            assert False\n    assert fake.call_count==expected\ntry:\n    retry_json(base_url,0)\nexcept ValueError:\n    pass\nelse:\n    assert False')],['Validate attempts first.','Catch HTTPError inside the loop.','Raise when the status is not 503 or the last attempt failed.'],'A retry policy needs a stopping condition and an explicit list of retryable failures.',files=fixture,review=['apis-errors'])
    unit(m,'report-project','Project · reconcile an API export','Build a complete local API report. Fetch both pages and produce a JSON audit with the record count and total amount. The exported file should contain ordinary numbers and can be downloaded from Output files. First inspect a response, then implement collection, then compute the summary.',http+fetch,['Fetch every order. Write api_report.json with count 3 and total 35, calculated from the records.'],http+'\n# Build your report',http+fetch+pages+'\norders=all_orders()\nreport={"count":len(orders),"total":sum(row["amount"] for row in orders)}\nwith open("api_report.json","w") as file:\n    json.dump(report,file)',[('Export a complete report','import json\nassert json.load(open("api_report.json"))=={"count":3,"total":35}\nimport practice_api\nassert any("page=2" in path for path in practice_api.requests)')],['Reuse your pagination pattern.','Compute count and sum from collected rows.','Use json.dump inside a with block.'],'You combined a client, collection logic, and a portable output.',kind='project',minutes=30,files=fixture,exports=['api_report.json'],review=['apis-pages','files-json'])

    m=section('engineering','Reliable Python programs','Test behavior and organise a project across files.','Build a tested report tool',[
        ('Tests are examples with consequences','self.assertEqual(total([2,3]),5)','Test normal input, boundary cases, and invalid data. A test should fail when behavior is wrong.'),
        ('Replace external dependencies','def report(loader):\n    return sum(loader())','Accept a dependency as a parameter so tests can provide controlled input.'),
        ('Multiple files','from calculations import total','Click a filename above the editor to change files. Submit runs main.py together with your saved companion files.')])
    unit(m,'unittest','Write tests that catch a boundary bug','unittest groups checks into TestCase classes. Your test will be run against a correct implementation and two buggy ones. Write meaningful input/output assertions, especially at the free-shipping boundary. Do not call unittest.main(): Pyroom runs the test suite during submission.', 'import unittest\nclass Example(unittest.TestCase):\n    def test_value(self):\n        self.assertEqual(2+2,4)',['Define ShippingTests(unittest.TestCase) with a test for shipping(0), shipping(49), shipping(50), and shipping(80). Expected results: 4,4,0,0.'], 'import unittest\n\ndef shipping(total):\n    return 0 if total >= 50 else 4\n\nclass ShippingTests(unittest.TestCase):\n    pass', 'import unittest\n\ndef shipping(total):\n    return 0 if total >= 50 else 4\n\nclass ShippingTests(unittest.TestCase):\n    def test_boundaries(self):\n        for value, expected in [(0,4),(49,4),(50,0),(80,0)]:\n            self.assertEqual(shipping(value), expected)',[('Tests accept correct code and detect bugs','from unittest.mock import patch\ndef run_tests(candidate):\n    with patch.dict(__learner_globals__,{"shipping":candidate}):\n        suite=unittest.defaultTestLoader.loadTestsFromTestCase(ShippingTests)\n        result=unittest.TestResult()\n        suite.run(result)\n        assert result.testsRun>0\n        return result.wasSuccessful()\nassert run_tests(lambda x:0 if x>=50 else 4)\nassert not run_tests(lambda x:0 if x>50 else 4)\nassert not run_tests(lambda x:0)')],['Methods must start with test_.','Use self.assertEqual.','Include both sides of the boundary and the boundary itself.'],'These tests distinguish behavior instead of checking the implementation text.',review=['bridge-contract'])
    unit(m,'dependencies','Inject a data loader','A report that always reads a particular file is awkward to test. Passing a loader function separates input from calculation. Your function calls the loader exactly once, sums its values, and returns a dictionary. Tests can use lambdas without creating files or making requests.', 'def count_rows(loader):\n    return len(loader())',['Write summarise(loader), returning {"count": number of values, "total": sum}. Call loader once.'],'def summarise(loader):\n    pass','def summarise(loader):\n    values=loader()\n    return {"count":len(values),"total":sum(values)}',[('Handle controlled and empty inputs','from unittest.mock import Mock\nloader=Mock(return_value=[2,-1,0])\nassert summarise(loader)=={"count":3,"total":1}\nloader.assert_called_once_with()\nassert summarise(lambda:[])=={"count":0,"total":0}')],['Call loader() and store its result.','Calculate count and total from the stored values.','Return a dictionary.'],'The function is easier to reuse and test because input is a separate responsibility.',review=['functions-return'])
    unit(m,'arguments','Parse command-line options','argparse converts a list of command-line strings into named settings. Passing argv explicitly makes a command-line interface testable inside this editor. Give input a default filename and add a flag for a dry run. A dry run lets an automation explain its work before writing outputs.', 'import argparse\np=argparse.ArgumentParser()\np.add_argument("--name", default="friend")\nprint(p.parse_args([]).name)',['Define options(argv), returning parsed arguments with --input defaulting to sales.csv and --dry-run as a store_true flag.'],'import argparse\n\ndef options(argv):\n    pass','import argparse\n\ndef options(argv):\n    parser=argparse.ArgumentParser()\n    parser.add_argument("--input",default="sales.csv")\n    parser.add_argument("--dry-run",action="store_true")\n    return parser.parse_args(argv)',[('Parse defaults and custom settings','assert options([]).input=="sales.csv" and options([]).dry_run is False\nr=options(["--input","other.csv","--dry-run"])\nassert r.input=="other.csv" and r.dry_run is True')],['Create an ArgumentParser.','Use action="store_true" for the flag.','Return parser.parse_args(argv).'],'Explicit argument lists let you practise command-line tools without opening a terminal.',review=['automation-paths'])
    unit(m,'logging','Log a useful audit message','Logging records events at a severity level. Accept a logger so the caller controls where events are written. Your function should ignore negative values and issue one warning per rejected value. Keep zero and positive numbers. Tests inspect log calls independently from the returned result.', 'import logging\nlogger=logging.getLogger("report")\nlogger.warning("Rejected value: %s", -1)',['Write keep_nonnegative(values, logger). Return nonnegative values in input order and call logger.warning once per rejected value.'],'def keep_nonnegative(values, logger):\n    pass','def keep_nonnegative(values, logger):\n    accepted=[]\n    for value in values:\n        if value<0:\n            logger.warning("Rejected value: %s",value)\n        else:\n            accepted.append(value)\n    return accepted',[('Keep good data and log exclusions','from unittest.mock import Mock\nlog=Mock()\nassert keep_nonnegative([0,-2,5,-1],log)==[0,5]\nassert log.warning.call_count==2\nlog.reset_mock()\nassert keep_nonnegative([],log)==[]\nlog.warning.assert_not_called()')],['Loop through each value.','Append values >= 0.','Call warning for each negative value.'],'The caller can route logs to a file, console, or test double.',review=['analysis-audit-review'])
    unit(m,'modules','Split calculation from presentation','A Python file can provide reusable functions to another file. Keep calculation in calculations.py and import it from main.py. The companion file is editable through the filename tabs. Pyroom executes your saved versions together, so unfinished helper code affects the submitted result.', 'from calculations import total\nprint(total([2,3]))',['In calculations.py define total(values), returning their sum.', 'In main.py import total and assign answer=total([10,-2,0]).'],'from calculations import total\n\n# Calculate answer here','from calculations import total\nanswer=total([10,-2,0])',[('Import and use the helper','import calculations\nassert calculations.total([1,2,3])==6\nassert calculations.total([])==0\nassert answer==8')],['Open calculations.py above the editor.','Return sum(values).','Import the function in main.py.'],'Separating a reusable operation makes it usable in scripts, tests, and web apps.',editors={'calculations.py':'def total(values):\n    pass'},solutions={'calculations.py':'def total(values):\n    return sum(values)'},review=['engineering-dependencies'])
    helper='''
def clean_amounts(texts):
    import math
    values=[]
    for text in texts:
        try:
            value=float(text)
            if math.isfinite(value):
                values.append(value)
        except ValueError:
            pass
    return values
'''
    unit(m,'tool-project','Project · build a reusable reporting tool','Create a small program with a reusable cleaning function and a thin entry point. The helper accepts finite numeric strings, including refunds and zeros. The entry point reads amounts.txt and writes a JSON summary. The same helper must work with new inputs, which is why hidden checks call it directly.', 'from cleaning import clean_amounts\nvalues=clean_amounts(["2","bad"])',['Implement clean_amounts(texts) in cleaning.py. Ignore invalid and nonfinite numbers.', 'Read amounts.txt in main.py and export summary.json containing count and total.'],'from cleaning import clean_amounts\n\n# Read, summarise, and export','import json\nfrom cleaning import clean_amounts\nvalues=clean_amounts(open("amounts.txt").read().splitlines())\nwith open("summary.json","w") as file:\n    json.dump({"count":len(values),"total":sum(values)},file)',[('Reuse the cleaning function','from cleaning import clean_amounts\nassert clean_amounts(["0","-2","oops","nan","inf"])==[0.0,-2.0]\nassert clean_amounts([])==[]'),('Export the summary','import json\nassert json.load(open("summary.json"))=={"count":3,"total":8}')],['Convert each line with float inside try/except.','Use math.isfinite.','Keep file reading and export in main.py.'],'The reusable helper has no knowledge of filenames or presentation.',kind='project',minutes=30,files={'amounts.txt':'10\n-2\n0\nbad\nnan\n'},editors={'cleaning.py':'def clean_amounts(texts):\n    pass'},solutions={'cleaning.py':helper},exports=['summary.json'],review=['engineering-modules','bridge-refunds'])

    m=section('flask','Build local web applications','Routes, forms, escaped templates, and persistent records.','Make a local task tracker',[
        ('Routes','app=Flask(__name__)\n@app.get("/")\ndef home():\n    return "Hello"','Define app but do not call app.run(). Submit uses Flask’s test client; Preview app hosts your app on a temporary local address.'),
        ('Forms and redirects','name=request.form.get("name", "").strip()\nreturn redirect(url_for("home"))','Use url_for for links and form actions so they work at the local preview address. Browser form submissions send strings.'),
        ('Template escaping','render_template_string("<p>{{ name }}</p>", name=name)','Jinja escapes values passed into HTML templates. Keep HTML structure separate from untrusted text. The preview database lasts until you start another preview or stop Pyroom.')])
    flask='from flask import Flask, request, render_template_string, redirect, url_for\napp=Flask(__name__)\n'
    unit(m,'route','Serve your first Flask route','Flask maps HTTP paths to Python functions. A route returns a response for the browser. In this exercise define a root route that returns a small HTML greeting. Submit checks the route without starting a server; Preview app opens the same app on your computer.',flask+'\n@app.get("/")\ndef home():\n    return "<h1>Hello</h1>"',['Create app and a GET / route returning an h1 containing Hello, Python!. Do not call app.run().'],flask,flask+'\n@app.get("/")\ndef home():\n    return "<h1>Hello, Python!</h1>"',[('Serve the root page','response=app.test_client().get("/")\nassert response.status_code==200\nassert "<h1>Hello, Python!</h1>" in response.text')],['Use @app.get("/").','Define the function below its decorator.','Return the HTML string.'],'A route is a function selected by an HTTP request.',web=True,review=['web-responses'])
    unit(m,'query','Read a query parameter in a route','request.args provides URL query values. Read name with a default, then return a JSON dictionary. Flask serializes the dictionary and sets the JSON response type. Query values are strings, even if they look numeric.', 'name=request.args.get("name","friend")',['Create GET /greet returning {"message": "Hello, <name>!"}. Default name is friend.'],flask,flask+'\n@app.get("/greet")\ndef greet():\n    name=request.args.get("name","friend")\n    return {"message":f"Hello, {name}!"}',[('Handle default and supplied names','client=app.test_client()\nassert client.get("/greet").json=={"message":"Hello, friend!"}\nassert client.get("/greet",query_string={"name":"Mei & Bo"}).json=={"message":"Hello, Mei & Bo!"}')],['Use request.args.get.','Use the default friend.','Return a dictionary.'],'Flask handles JSON serialization while your route defines the response meaning.',web=True,review=['apis-query'])
    unit(m,'templates','Render user text safely','A template defines HTML separately from values. Jinja replaces {{ name }} and escapes HTML-special characters. Concatenating raw input into HTML can cause it to become markup. Pass name as a template variable, then try a name containing angle brackets.', 'render_template_string("<h1>Hello, {{ name }}!</h1>",name="Mei")',['Create GET /, read name with default friend, and render an h1 greeting using render_template_string.'],flask,flask+'\n@app.get("/")\ndef home():\n    return render_template_string("<h1>Hello, {{ name }}!</h1>",name=request.args.get("name","friend"))',[('Render a greeting and escape markup','client=app.test_client()\nassert "Hello, friend!" in client.get("/").text\nresponse=client.get("/",query_string={"name":"<script>alert(1)</script>"})\nassert "<script>" not in response.text\nassert "&lt;script&gt;" in response.text')],['Keep {{ name }} in the template string.','Pass name as a keyword argument.','Do not use an f-string to insert user text into HTML.'],'Template variables preserve text as text.',web=True,review=['web-html-list'])
    form='''
@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        name=request.form.get('name','').strip()
        if not name:
            return 'Name is required',400
        return redirect(url_for('hello',name=name))
    return render_template_string('<form method="post" action="{{ url_for(\'home\') }}"><label>Name <input name="name"></label><button>Greet</button></form>')

@app.get('/hello')
def hello():
    return render_template_string('<h1>Hello, {{ name }}!</h1>',name=request.args.get('name','friend'))
'''
    # Triple-quoted HTML avoids nested Python string escaping in learner code.
    form=form.replace("render_template_string('<form", 'render_template_string("""<form').replace("</form>')", '</form>""")')
    unit(m,'forms','Validate a submitted form','A form sends values with POST. Validate the submitted name on the server because browser checks can be bypassed. On success redirect to a GET page; this prevents a normal refresh from repeating the POST. url_for builds a link that also works under Pyroom’s preview prefix.', 'name=request.form.get("name", "").strip()\nif not name:\n    return "Name is required",400',['Create GET / with a POST form containing a name input.', 'POST / rejects blank names with 400, otherwise redirects to /hello?name=... . GET /hello renders an escaped greeting.'],flask,flask+form,[('Show and validate the form','client=app.test_client()\nassert "<form" in client.get("/").text\nassert client.post("/",data={"name":"  "}).status_code==400'),('Redirect and greet','response=client.post("/",data={"name":" Mei "})\nassert response.status_code in (302,303)\nassert "Hello, Mei!" in client.get(response.headers["Location"]).text')],['Use one route with methods GET and POST.','Strip the form value before validation.','Use redirect(url_for("hello",name=name)).'],'The form has a complete request, validation, redirect, and display flow.',web=True,minutes=25,review=['flask-templates'])
    db='''
import sqlite3
with sqlite3.connect('notes.db') as db:
    db.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, text TEXT NOT NULL)')
'''
    routes='''
@app.route('/notes',methods=['GET','POST'])
def notes():
    with sqlite3.connect('notes.db') as db:
        if request.method=='POST':
            text=request.form.get('text','').strip()
            if not text:
                return {'error':'text required'},400
            db.execute('INSERT INTO notes(text) VALUES (?)',(text,))
            return {'saved':True},201
        rows=db.execute('SELECT text FROM notes ORDER BY id').fetchall()
    return {'notes':[row[0] for row in rows]}
'''
    unit(m,'database','Persist records with SQLite','A Python list disappears when a process restarts. SQLite stores records in a local database file. Open a connection for each operation, use parameter placeholders, and commit writes with a connection context manager. The practice database is fresh for each Run or Submit; a preview keeps its database between browser requests.',db,['Implement GET /notes returning {"notes": list of texts in insertion order}.', 'POST /notes reads text, rejects blank with 400, otherwise inserts and returns {"saved": true} with 201.'],flask+db,flask+db+routes,[('Store and retrieve records','client=app.test_client()\nassert client.get("/notes").json=={"notes":[]}\nassert client.post("/notes",data={"text":"  "}).status_code==400\nfor text in ["Read","Bo\'s note"]:\n    assert client.post("/notes",data={"text":text}).status_code==201\nassert client.get("/notes").json=={"notes":["Read","Bo\'s note"]}')],['Branch on request.method.','Use INSERT with a ? placeholder.','Query ORDER BY id and convert rows to texts.'],'Data persists independently of a particular request.',web=True,minutes=25,review=['sql-parameters','sql-transaction'])
    tracker='''
import sqlite3
with sqlite3.connect('tasks.db') as db:
    db.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)')

@app.route('/',methods=['GET','POST'])
def home():
    with sqlite3.connect('tasks.db') as db:
        if request.method=='POST':
            title=request.form.get('title','').strip()
            if not title:
                return 'Title required',400
            db.execute('INSERT INTO tasks(title) VALUES (?)',(title,))
            return redirect(url_for('home'))
        rows=db.execute('SELECT id,title FROM tasks ORDER BY id').fetchall()
    return render_template_string("""<h1>My tasks</h1><form method="post" action="{{ url_for('home') }}"><label>Task <input name="title"></label><button>Add</button></form><ul>{% for id,title in rows %}<li>{{ title }}</li>{% endfor %}</ul>""",rows=rows)
'''
    unit(m,'tracker-project','Project · your local task tracker','Combine a real HTML form, validation, a database, and a rendered list. Build one root route handling GET and POST. Keep records in tasks.db so they survive multiple requests in the same preview. After passing, use Preview app to add your own tasks and refresh the page.', 'rows=db.execute("SELECT id,title FROM tasks ORDER BY id").fetchall()',['GET / shows an Add form with title input and all stored task titles.', 'POST / validates a nonblank title, inserts into tasks.db, then redirects to /. Blank titles return 400.', 'Render titles with template escaping and insertion order.'],flask,flask+tracker,[('Validate and persist task titles','client=app.test_client()\nassert "<form" in client.get("/").text\nassert client.post("/",data={"title":" "}).status_code==400\nfor title in ["Learn SQL","<b>Read</b>"]:\n    response=client.post("/",data={"title":title})\n    assert response.status_code in (302,303)\npage=client.get("/").text\nassert "Learn SQL" in page and "&lt;b&gt;Read&lt;/b&gt;" in page\nassert "<b>Read</b>" not in page\nimport sqlite3\nwith sqlite3.connect("tasks.db") as db:\n    assert db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]==2')],['Create the table with IF NOT EXISTS.','Use placeholders for the insert.','Pass rows to a Jinja loop and use url_for in the form.'],'You built a complete local web workflow with durable records for the preview session.',web=True,kind='project',minutes=40,review=['flask-forms','flask-database'])

    m=section('capstones','Independent projects','Work from a brief and combine several modules.', 'Three portfolio-sized starting points',[
        ('Plan before coding','# Inputs → validation → transformation → outputs','Write a checklist from the brief. Build and run one part at a time; use hints only after trying an approach.'),
        ('Inspect the result','# Reconcile source rows, exclusions, and totals','Passing checks verifies the stated contract. Open exported files and try your own data or browser inputs to assess usability.')])
    unit(m,'analysis','Independent project · sales reporting pack','Your team needs a clean regional sales report from a messy export. Build a reproducible analysis that explains exclusions, calculates totals, and communicates the result with both a chart and a spreadsheet. This project supplies the brief and data, with fewer scaffolding steps than earlier lessons.', 'clean.groupby("region")["amount"].sum()',['Read sales.csv. Strip and lowercase region. Reject blank regions and amounts that are invalid, nonfinite, or negative; retain zero.', 'Write report.xlsx with sheet Summary and columns region, amount, sorted by region.', 'Create a labelled bar chart of regional totals as report.png. Write audit.json with accepted and rejected counts.'], '# Build your reporting pack here','''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
data=pd.read_csv('sales.csv')
data['region']=data['region'].fillna('').str.strip().str.lower()
data['amount']=pd.to_numeric(data['amount'],errors='coerce')
mask=data['region'].ne('') & np.isfinite(data['amount']) & data['amount'].ge(0)
clean=data[mask]
summary=clean.groupby('region',as_index=False)['amount'].sum().sort_values('region')
summary.to_excel('report.xlsx',sheet_name='Summary',index=False)
fig,ax=plt.subplots()
ax.bar(summary['region'],summary['amount'])
ax.set(title='Regional sales',xlabel='Region',ylabel='Revenue')
fig.savefig('report.png')
with open('audit.json','w') as file:
    json.dump({'accepted':int(mask.sum()),'rejected':int((~mask).sum())},file)
''',[('Reconcile and export the data','import json,pandas as pd\nassert json.load(open("audit.json"))=={"accepted":3,"rejected":4}\nrows=pd.read_excel("report.xlsx",sheet_name="Summary").to_dict("records")\nassert rows==[{"region":"north","amount":30},{"region":"south","amount":0}]'),('Create a labelled chart','from pathlib import Path\nassert Path("report.png").read_bytes()[:4]==bytes([137,80,78,71])\nassert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()\nassert sorted(round(p.get_height(),2) for p in ax.patches)==[0,30]')],['Convert amount with errors="coerce" and build one Boolean mask.','Group accepted records and export with index=False.','Use the same summary for your chart and report.'], 'The chart, spreadsheet, and audit reconcile to one validated dataset.',kind='project',minutes=60,files={'sales.csv':'region,amount\n North ,10\nnorth,20\nSouth,0\nWest,-1\nEast,bad\n,5\nSouth,inf\n'},exports=['report.xlsx','report.png','audit.json'],review=['wrangling-monthly-project','charts-bar','excel-workbook-project'])
    unit(m,'automation','Independent project · batch file audit','Several text exports arrive in an inbox. Build a reusable cleaner and an entry point that processes every .txt file in alphabetical order. Accept finite decimal numbers including refunds and zeros. Record one summary per file, including rejected lines. The helper must remain reusable with different input.', 'for path in sorted(Path("inbox").glob("*.txt")):\n    print(path.name)',['Implement audit(texts) in audit.py returning count, rejected, total (rounded to two decimals).', 'In main.py process inbox/*.txt alphabetically. Export batch.json as a list of dictionaries with file, count, rejected, total.'], 'from audit import audit\n\n# Process the inbox', '''
import json
from pathlib import Path
from audit import audit
reports=[]
for path in sorted(Path('inbox').glob('*.txt')):
    reports.append({'file':path.name,**audit(path.read_text().splitlines())})
Path('batch.json').write_text(json.dumps(reports))
''',[('Support new inputs','from audit import audit\nassert audit(["1.5","-2","0","inf","bad"])=={"count":3,"rejected":2,"total":-0.5}\nassert audit([])=={"count":0,"rejected":0,"total":0}'),('Audit every input file','import json\nassert json.load(open("batch.json"))==[{"file":"a.txt","count":2,"rejected":1,"total":8},{"file":"b.txt","count":1,"rejected":2,"total":0}]')],['Use the finite-number cleaning pattern.','Calculate rejected as input length minus accepted length.','Keep directory traversal in main.py.'],'Each output row explains exactly what happened to one source file.',kind='project',minutes=60,files={'inbox/a.txt':'10\n-2\nbad\n','inbox/b.txt':'0\nnan\noops\n'},editors={'audit.py':'def audit(texts):\n    pass'},solutions={'audit.py':helper+'\ndef audit(texts):\n    values=clean_amounts(texts)\n    return {"count":len(values),"rejected":len(texts)-len(values),"total":round(sum(values),2)}'},exports=['batch.json'],review=['engineering-tool-project','automation-paths'])
    inventory='''
import sqlite3
with sqlite3.connect('inventory.db') as db:
    db.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT NOT NULL, quantity INTEGER NOT NULL)')

@app.route('/',methods=['GET','POST'])
def home():
    with sqlite3.connect('inventory.db') as db:
        if request.method=='POST':
            name=request.form.get('name','').strip()
            try:
                quantity=int(request.form.get('quantity',''))
                if not name or quantity<0:
                    raise ValueError()
            except ValueError:
                return 'Enter a name and nonnegative whole quantity',400
            db.execute('INSERT INTO items(name,quantity) VALUES (?,?)',(name,quantity))
            return redirect(url_for('home'))
        rows=db.execute('SELECT name,quantity FROM items ORDER BY id').fetchall()
    return render_template_string("""<h1>Local inventory</h1><form method="post" action="{{ url_for('home') }}"><label>Name <input name="name"></label><label>Quantity <input name="quantity" type="number" min="0"></label><button>Add item</button></form><ul>{% for name,quantity in rows %}<li>{{ name }}: {{ quantity }}</li>{% endfor %}</ul>""",rows=rows)
'''
    unit(m,'web','Independent project · inventory notebook','Build a useful local inventory app. Users add a named item and a whole-number quantity, then see the stored records. Validation belongs on the server as well as the form. Keep HTML text escaped, use bound SQL values, and redirect after a successful insert. Once it passes, try realistic item names in Preview app.', 'quantity=int(request.form.get("quantity",""))',['GET / shows an HTML form with name and quantity inputs and the stored records in insertion order.', 'POST / accepts a stripped nonblank name and an integer quantity >= 0; otherwise returns 400.', 'Persist records in inventory.db table items with name and quantity columns. Redirect to / after success and escape displayed names.'],flask,flask+inventory,[('Reject invalid submissions','client=app.test_client()\nassert "<form" in client.get("/").text\nfor name,quantity in [(" ","1"),("Tea","-1"),("Tea","1.5"),("Tea","oops")]:\n    assert client.post("/",data={"name":name,"quantity":quantity}).status_code==400'),('Persist valid records and escape names','for name,quantity in [("Tea","2"),("<b>Cake</b>","0")]:\n    assert client.post("/",data={"name":name,"quantity":quantity}).status_code in (302,303)\npage=client.get("/").text\nassert "Tea" in page and "&lt;b&gt;Cake&lt;/b&gt;" in page and "<b>Cake</b>" not in page\nimport sqlite3\nwith sqlite3.connect("inventory.db") as db:\n    assert db.execute("SELECT name,quantity FROM items ORDER BY id").fetchall()==[("Tea",2),("<b>Cake</b>",0)]')],['Build the table and GET page first.','Validate conversion inside try/except before inserting.','Reuse the redirect and template loop from the task tracker.'],'You now have a foundation for a personal app with forms, validation, persistence, and automated checks.',kind='project',minutes=75,web=True,review=['flask-tracker-project','sql-parameters'])
