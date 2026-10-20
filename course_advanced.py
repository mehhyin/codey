"""Practice beyond the foundations: original problems, datasets and graders."""


def extend_advanced(section, unit):
    m = section('toolbox', 'Sequences, generators and callbacks',
        'Build reusable tools that handle unfamiliar inputs.',
        'Audit a stream of sensor messages', 'advanced', [
            ('Lazy iteration', 'def squares(values):\n    for value in values:\n        yield value ** 2',
             'A generator produces values on demand. Creating it does not consume the input.'),
            ('A function as input', 'def apply(value, transform):\n    return transform(value)',
             'A callback separates the mechanics of iteration from the operation to perform.'),
            ('Full text matching', 'import re\nvalid = re.fullmatch(r"[A-Z]{2}", "AB") is not None',
             'fullmatch requires the entire string to match; search accepts a matching substring.')
        ], ['functions-return', 'collections-lists', 'functions-validation'])
    unit(m, 'runs', 'Compress consecutive readings',
        'Repeated adjacent values often represent one continuous event. Run-length encoding stores each value with the length of its consecutive run. Equal values separated by another value belong to different runs. Build a fresh result rather than modifying the observations.',
        'events = ["open", "open", "closed"]\n# A run describes adjacent equal events, not total frequency.',
        ['Define `runs(values)`, accepting a list of numbers or strings.',
         'Return a list of `(value, count)` tuples describing consecutive equal values, from left to right.',
         'For `["a", "a", "b", "a"]`, return `[("a", 2), ("b", 1), ("a", 1)]`. Return `[]` for empty input and leave the input unchanged.'],
        '''
        def runs(values):
            result = []
            for value in values:
                if result and result[-1][0] == value:
                    result[-1] = (value, result[-1][1] + 1)
                else:
                    result.append((value, 1))
            return result
        ''',
        [('Separate nonadjacent repeats', 'assert runs(["a","a","b","a"]) == [("a",2),("b",1),("a",1)]'),
         ('Handle numbers, empty input and preserve data', '''
          source = [0,0,-1,-1,-1,0]
          assert runs(source) == [(0,2),(-1,3),(0,1)]
          assert source == [0,0,-1,-1,-1,0] and runs([]) == []
          assert runs(["x"]) == [("x",1)]
          ''')],
        ['Compare each observation with the most recent run.', 'Extend the last run only when its value matches.', 'Remember that an empty result has no last entry.'],
        'Run counts describe consecutive behavior; a frequency table would lose the order of events.')
    unit(m, 'windows', 'Slide a window across observations',
        'A sliding window groups neighboring observations without skipping any starting position. This supports moving statistics and pattern detection. A width of three across five values produces three complete windows. Partial windows at the end are excluded.',
        'values = [3, 5, 7]\nfirst_pair = values[0:2]\n# Slicing creates a new list.',
        ['Define `windows(values, width)`, where `values` is a list and `width` is an integer.',
         'Return a list of lists containing every consecutive window of exactly `width` items, in input order.',
         'Raise `ValueError` when `width` is zero or negative. Return `[]` when the list is shorter than the width. Do not change `values`.'],
        '''
        def windows(values, width):
            if width <= 0:
                raise ValueError("width must be positive")
            return [values[i:i+width] for i in range(len(values)-width+1)]
        ''',
        [('Include overlapping windows', 'assert windows([2,4,6,8],2) == [[2,4],[4,6],[6,8]]\nassert windows([9,3],1) == [[9],[3]]'),
         ('Check boundaries and independence', '''
          assert windows([],2) == [] and windows([1],3) == []
          for width in [0,-2]:
              try: windows([1],width)
              except ValueError: pass
              else: raise AssertionError("Expected ValueError")
          source = [1,2,3]
          result = windows(source,2); result[0][0] = 99
          assert source == [1,2,3]
          ''')],
        ['Count how many starting positions leave room for a complete window.', 'Use a separate slice for each starting position.', 'Validate width before constructing the result.'],
        'Separating window construction from later calculations lets several analyses reuse the same function.')
    unit(m, 'batches', 'Process a stream in batches',
        'An iterator may represent data too large to store all at once. A generator can group a stream into bounded batches, yielding one batch before reading the next. The final batch may be shorter. Generator validation runs when iteration begins, not necessarily when the generator object is created.',
        'def repeat_twice(items):\n    for item in items:\n        yield item\n        yield item',
        ['Define the generator function `batches(items, size)`, accepting any iterable and a positive integer batch size.',
         'Yield lists of up to `size` items, preserving order. Yield a final partial batch if needed; yield nothing for empty input.',
         'Do not consume the whole iterable up front. Raise `ValueError` for `size <= 0` when iteration begins.'],
        '''
        def batches(items, size):
            if size <= 0:
                raise ValueError("size must be positive")
            batch = []
            for item in items:
                batch.append(item)
                if len(batch) == size:
                    yield batch
                    batch = []
            if batch:
                yield batch
        ''',
        [('Retain partial batches and accept iterators', 'assert list(batches(iter([1,2,3,4,5]),2)) == [[1,2],[3,4],[5]]\nassert list(batches([],3)) == []'),
         ('Consume lazily and reject invalid sizes', '''
          import inspect
          assert inspect.isgeneratorfunction(batches)
          seen = []
          def source():
              for n in range(7):
                  seen.append(n)
                  yield n
          stream = batches(source(),3)
          assert seen == []
          assert next(stream) == [0,1,2] and seen == [0,1,2]
          for size in [0,-1]:
              try: list(batches([1],size))
              except ValueError: pass
              else: raise AssertionError("Expected ValueError")
          ''')],
        ['Keep only the current batch in memory.', 'After yielding a full batch, create a new empty list.', 'Handle the remaining batch after the loop.'],
        'Lazy batches let a caller control how much of a stream is consumed.')
    unit(m, 'callbacks', 'Make a transformation configurable',
        'Functions are values that can be passed as arguments. A reusable processing function can accept one callback that decides which records to keep and another that transforms them. Checking eligibility before transformation avoids processing excluded data.',
        'def triple(number):\n    return number * 3\noperation = triple\nanswer = operation(4)',
        ['Define `select_map(items, keep, transform)`. `keep(item)` returns a Boolean; `transform(item)` returns a replacement value.',
         'Return a list of transformed items for which `keep` is true, in input order.',
         'Call `keep` once for each item and `transform` once for each kept item only. Accept iterators and return `[]` for empty input.'],
        '''
        def select_map(items, keep, transform):
            return [transform(item) for item in items if keep(item)]
        ''',
        [('Use different callbacks', 'assert select_map([1,2,3,4],lambda x:x%2==0,lambda x:x*x) == [4,16]\nassert select_map(iter(["a","","bb"]),bool,len) == [1,2]'),
         ('Transform only retained items', '''
          calls = []
          def keep(x):
              calls.append(("keep",x))
              return x > 0
          def transform(x):
              calls.append(("transform",x))
              return 10/x
          assert select_map([0,2],keep,transform) == [5]
          assert calls == [("keep",0),("keep",2),("transform",2)]
          assert select_map([],keep,transform) == []
          ''')],
        ['Treat both callbacks like ordinary callable functions.', 'Filter before applying the transformation.', 'Avoid making a second pass over a one-use iterator.'],
        'Callbacks make the control flow reusable while letting callers choose the business rule.')
    unit(m, 'codes', 'Validate complete reference codes',
        'Text validation differs from text searching. A valid code must match the whole format, not just contain a valid substring. Regular expression character classes describe allowed characters; anchors or fullmatch enforce the boundary. Restricting digits to 0–9 avoids accepting other Unicode digit characters unintentionally.',
        'import re\nis_pair = re.fullmatch(r"[A-Z]{2}", "QR") is not None',
        ['Define `valid_code(text)` and return a Boolean.',
         'Accept exactly three uppercase ASCII letters, one hyphen, and four ASCII digits. The first digit must be 1–9; the remaining digits may be 0–9.',
         'Reject spaces, lowercase letters, extra characters and trailing newlines. Assume `text` is a string; do not strip it.'],
        '''
        import re
        def valid_code(text):
            return re.fullmatch(r"[A-Z]{3}-[1-9][0-9]{3}", text) is not None
        ''',
        [('Accept full valid codes', 'assert valid_code("QRS-1200") is True and valid_code("ABC-9999") is True'),
         ('Reject partial matches and invalid characters', '''
          for text in ["QRS-0123","qrs-1200"," QRS-1200","QRS-1200\\n","XQRS-1200","QRS-１２３４","QRS-12",""]:
              assert valid_code(text) is False, text
          ''')],
        ['Describe each segment of the code separately.', 'The first digit has a different range from the others.', 'Use fullmatch rather than search.'],
        'A validator enforces the entire input contract, including whitespace and character ranges.')
    unit(m, 'stream-project', 'Project · audit sensor messages',
        'A monitoring export contains one station and one measurement per line. Combine parsing, validation and grouping into a reusable audit function. Invalid data must be counted rather than silently converted to zero. The input is a stream, so consume it only once.',
        'record = "north|18.5"\nparts = record.split("|")\n# Parsing alone does not establish that a record is valid.',
        ['Define `audit_messages(lines)`, accepting an iterable of strings. Each valid line contains exactly one `|`, separating a nonblank station from a finite numeric reading.',
         'Strip both fields and lowercase station names. Accept negative readings and zero. Reject missing or extra separators, blank fields, invalid numeric text, `NaN` and infinities.',
         'Return a dictionary with `accepted`, `rejected`, and `means`. `means` maps each cleaned station to its average reading rounded to two decimals. For empty input use zero counts and an empty dictionary.',
         'Read `messages.txt`, call your function, and write the returned dictionary as JSON to `sensor_audit.json`.'],
        '''
        import json
        import math
        def audit_messages(lines):
            groups = {}
            accepted = rejected = 0
            for line in lines:
                fields = line.split("|")
                try:
                    if len(fields) != 2 or not fields[0].strip():
                        raise ValueError()
                    value = float(fields[1].strip())
                    if not math.isfinite(value):
                        raise ValueError()
                    station = fields[0].strip().lower()
                    groups.setdefault(station, []).append(value)
                    accepted += 1
                except ValueError:
                    rejected += 1
            return {"accepted": accepted, "rejected": rejected,
                    "means": {name: round(sum(v)/len(v),2) for name,v in groups.items()}}
        with open("messages.txt",encoding="utf-8") as f:
            report = audit_messages(f)
        with open("sensor_audit.json","w",encoding="utf-8") as f:
            json.dump(report,f)
        ''',
        [('Audit unseen and empty streams', '''
          assert audit_messages(iter([" West | 4","west|-2","east|0","bad","x|nan","|4","x|3|2"])) == {"accepted":3,"rejected":4,"means":{"west":1.0,"east":0.0}}
          assert audit_messages([]) == {"accepted":0,"rejected":0,"means":{}}
          assert audit_messages(["x|inf","x|-inf","x|","x|oops"])["rejected"] == 4
          '''),
         ('Save the supplied-file audit', '''
          import json
          with open("sensor_audit.json",encoding="utf-8") as f: saved = json.load(f)
          assert saved == {"accepted":4,"rejected":3,"means":{"roof":11.0,"yard":-1.0}}
          ''')],
        ['Validate both the record structure and numeric value.', 'Keep observations or a sum and count for each cleaned station.', 'Serialize the dictionary returned by your function, not a manually typed report.'],
        'An audit makes rejected records visible and leaves the valid statistics reproducible.',
        files={'messages.txt':' Roof | 10\nroof|12\nyard|-2\nyard|0\nroof|nan\nbad line\n|9\n'},
        exports=['sensor_audit.json'], kind='project', minutes=35)

    m = section('objects', 'Classes and stateful programs',
        'Model state, composition and reusable behavior.',
        'Build a library lending model', 'advanced', [
            ('Instance state', 'class Meter:\n    def __init__(self, value):\n        self.value = value\n    def read(self):\n        return self.value',
             'Store independent object state on self. A list on the class would be shared by every instance.'),
            ('Inheritance', 'class Sensor:\n    def label(self):\n        return "sensor"\nclass OutdoorSensor(Sensor):\n    pass',
             'A subclass inherits behavior and may override a method with a specialized implementation.'),
            ('Composition', 'class Station:\n    def __init__(self, sensor):\n        self.sensor = sensor',
             'One object can contain and coordinate another object without inheriting from it.')
        ], ['functions-validation', 'collections-dicts'])
    unit(m, 'counter', 'Give each object its own state',
        'A class defines how objects are created and how they behave. __init__ initializes each instance, and methods receive that instance as self. Separate instances should not accidentally share changing state.',
        'class Label:\n    def __init__(self, text):\n        self.text = text\nfirst = Label("Desk")',
        ['Define class `Counter`. `Counter(start=0)` stores the initial numeric value in public attribute `value`.',
         'Implement `add(amount=1)` to increase this instance’s value and return its new value. Allow zero and negative amounts.',
         'Implement `reset()` to restore this instance’s original start value and return that value. Separate counters must remain independent.'],
        '''
        class Counter:
            def __init__(self,start=0):
                self.start = start
                self.value = start
            def add(self,amount=1):
                self.value += amount
                return self.value
            def reset(self):
                self.value = self.start
                return self.value
        ''',
        [('Apply default and explicit increments', 'a=Counter(); assert a.value == 0 and a.add() == 1 and a.add(-3) == -2 and a.add(0) == -2'),
         ('Reset independently', 'a=Counter(5); b=Counter(10); a.add(2)\nassert b.value == 10 and a.reset() == 5 and a.value == 5\nassert b.reset() == 10')],
        ['Store the original value as well as the changing one.', 'Read and write instance attributes through self.', 'A reset restores the starting value, which is not always zero.'],
        'Instance attributes isolate state while the class shares method definitions.')
    unit(m, 'stock', 'Validate changes before applying them',
        'A method should reject an invalid change without partially updating its object. This is an invariant: a condition that must remain true after every operation. Here, stored inventory must always be a nonnegative integer.',
        'def require_positive(number):\n    if number <= 0:\n        raise ValueError("Expected a positive number")',
        ['Define `Stock(quantity=0)` with public attribute `quantity`. Accept only nonnegative integers; reject Booleans and all other values with `ValueError`.',
         'Implement `receive(amount)` and `take(amount)`. Each amount must be a positive integer, excluding Booleans. Reject an excessive withdrawal with `ValueError`.',
         'On success, return the new quantity. Any rejected operation must leave the quantity unchanged.'],
        '''
        class Stock:
            def __init__(self,quantity=0):
                if type(quantity) is not int or quantity < 0:
                    raise ValueError("Invalid quantity")
                self.quantity = quantity
            def receive(self,amount):
                if type(amount) is not int or amount <= 0:
                    raise ValueError("Invalid amount")
                self.quantity += amount
                return self.quantity
            def take(self,amount):
                if type(amount) is not int or amount <= 0 or amount > self.quantity:
                    raise ValueError("Invalid amount")
                self.quantity -= amount
                return self.quantity
        ''',
        [('Receive and withdraw valid stock', 's=Stock(2); assert s.receive(3)==5 and s.take(5)==0 and s.quantity==0'),
         ('Reject invalid input without changing state', '''
          for value in [-1,1.5,True,"2"]:
              try: Stock(value)
              except ValueError: pass
              else: raise AssertionError("Invalid initial quantity accepted")
          s=Stock(3)
          for method,amount in [(s.receive,0),(s.receive,True),(s.take,4),(s.take,-1),(s.take,1.5)]:
              try: method(amount)
              except ValueError: pass
              else: raise AssertionError("Invalid operation accepted")
              assert s.quantity==3
          ''')],
        ['Check types as well as numeric ranges.', 'Perform all validation before changing quantity.', 'bool is a subclass of int, so an exact type check is useful here.'],
        'Validation at the object boundary protects every caller from creating impossible state.')
    unit(m, 'ledger', 'Compose a ledger from entries',
        'Composition combines smaller pieces into a larger object. An expense ledger contains entries; it does not need to inherit from a list. Returning a copy of its records prevents callers from modifying its internal collection accidentally.',
        'records = [("tea", 4)]\ncopy = list(records)\ncopy.append(("cake", 6))\n# records still has one entry.',
        ['Define class `Ledger` with no constructor arguments and an initially empty collection.',
         'Implement `record(category, amount)` to append a `(category, amount)` tuple. Inputs are already valid strings and numbers; refunds may be negative.',
         'Implement `total(category=None)` to return the sum of all amounts, or only amounts matching the exact category when one is provided. Empty sums are zero.',
         'Implement `entries()` to return a new list of tuples in insertion order. Modifying that returned list must not modify the ledger.'],
        '''
        class Ledger:
            def __init__(self):
                self._entries = []
            def record(self,category,amount):
                self._entries.append((category,amount))
            def total(self,category=None):
                return sum(amount for name,amount in self._entries if category is None or name==category)
            def entries(self):
                return list(self._entries)
        ''',
        [('Summarise entries and refunds', 'l=Ledger(); assert l.total()==0\nl.record("food",8); l.record("travel",3); l.record("food",-2)\nassert l.total()==9 and l.total("food")==6 and l.total("other")==0'),
         ('Protect the collection and other instances', 'l=Ledger(); l.record("x",2)\nview=l.entries(); assert view==[("x",2)]\nview.clear(); assert l.entries()==[("x",2)] and Ledger().entries()==[]')],
        ['Use an instance list to store tuples.', 'None means no category filter.', 'Return a shallow copy because the stored tuples contain immutable values.'],
        'A small public interface can protect data while exposing useful operations.')
    unit(m, 'inheritance', 'Specialize a pricing rule',
        'Inheritance lets related types share an interface. An overridden method keeps its name and calling convention but changes the behavior. Code that calls the shared method can work with either type without checking its class.',
        'class Greeting:\n    def text(self):\n        return "Hello"\nclass CasualGreeting(Greeting):\n    def text(self):\n        return "Hi"',
        ['Define `RatePlan(rate)` and method `cost(hours)`, returning rate multiplied by hours.',
         'Define `CappedPlan(rate, cap)` as a subclass of `RatePlan`. Its `cost(hours)` returns the smaller of the ordinary cost and the cap.',
         'Inputs are nonnegative numbers. Do not round results or change stored rate/cap values when called.'],
        '''
        class RatePlan:
            def __init__(self,rate):
                self.rate=rate
            def cost(self,hours):
                return self.rate*hours
        class CappedPlan(RatePlan):
            def __init__(self,rate,cap):
                super().__init__(rate)
                self.cap=cap
            def cost(self,hours):
                return min(super().cost(hours),self.cap)
        ''',
        [('Preserve a shared interface', 'assert issubclass(CappedPlan,RatePlan)\nassert [p.cost(4) for p in [RatePlan(3),CappedPlan(3,8)]]==[12,8]'),
         ('Handle zero and costs below the cap', 'p=CappedPlan(2.5,10)\nassert p.cost(0)==0 and p.cost(2)==5 and p.cost(20)==10 and p.cost(1)==2.5\nassert RatePlan(0).cost(12)==0')],
        ['Initialize the base class with the hourly rate.', 'Override cost while keeping its parameter unchanged.', 'Compute the ordinary cost before applying the ceiling.'],
        'Polymorphism lets callers request the same operation from different pricing plans.')
    unit(m, 'protocols', 'Make a collection work with Python',
        'Python uses special methods for familiar operations: len(obj) calls __len__, iteration uses __iter__, and str(obj) uses __str__. Supporting these protocols makes a custom object easier to use in ordinary code.',
        'class Pair:\n    def __len__(self):\n        return 2\nprint(len(Pair()))',
        ['Define `Playlist(title, songs)`. Copy the supplied iterable of song titles into an instance collection.',
         'Support `len(playlist)` and iteration over its songs in the original order. Each new iteration must start from the beginning.',
         'Make `str(playlist)` return `<title> (<count> tracks)`, always using the word `tracks`. Later changes to the original songs list must not affect the playlist.'],
        '''
        class Playlist:
            def __init__(self,title,songs):
                self.title=title
                self.songs=list(songs)
            def __len__(self):
                return len(self.songs)
            def __iter__(self):
                return iter(self.songs)
            def __str__(self):
                return f"{self.title} ({len(self)} tracks)"
        ''',
        [('Support Python collection operations', 'p=Playlist("Focus",iter(["Rain","Wind"]))\nassert len(p)==2 and list(p)==["Rain","Wind"] and list(p)==["Rain","Wind"]\nassert str(p)=="Focus (2 tracks)"'),
         ('Copy input and handle an empty collection', 'songs=["A"]; p=Playlist("Solo",songs); songs.append("B")\nassert list(p)==["A"] and str(p)=="Solo (1 tracks)"\nassert len(Playlist("Empty",[]))==0')],
        ['Store a list so the iterable can be reused.', 'Return a fresh iterator over that list from __iter__.', 'Special method names have two underscores on each side.'],
        'Protocols let custom types participate in Python without making callers learn a separate API.')
    unit(m, 'library-project', 'Project · model library loans',
        'Build a small stateful model with clear failure behavior. A library owns a fixed catalog and tracks which books are on loan. Returning a book changes its availability, while queries should leave the model unchanged. This exercise combines instance state, validation and protected collections.',
        'catalog = {"B4": "Cloud Atlas", "A2": "The Workshop"}\n# IDs identify books even when titles repeat.',
        ['Define `Library(catalog)`, copying a dictionary mapping unique string book IDs to titles. All books start available.',
         'Implement `borrow(book_id)` to mark an available book as borrowed and return its title. Raise `KeyError` for an unknown ID and `ValueError` for an already borrowed book.',
         'Implement `give_back(book_id)` to make a borrowed book available and return its title. Raise `KeyError` for an unknown ID and `ValueError` if it is already available.',
         'Implement `available()` to return a new list of `(book_id, title)` tuples sorted by book ID. Rejected operations and changes to the original catalog must not alter the library.'],
        '''
        class Library:
            def __init__(self,catalog):
                self.catalog=dict(catalog)
                self.borrowed=set()
            def borrow(self,book_id):
                title=self.catalog[book_id]
                if book_id in self.borrowed:
                    raise ValueError("Already borrowed")
                self.borrowed.add(book_id)
                return title
            def give_back(self,book_id):
                title=self.catalog[book_id]
                if book_id not in self.borrowed:
                    raise ValueError("Already available")
                self.borrowed.remove(book_id)
                return title
            def available(self):
                return [(key,self.catalog[key]) for key in sorted(self.catalog) if key not in self.borrowed]
        ''',
        [('Complete a borrow and return cycle', 'l=Library({"B":"Birds","A":"Maps"})\nassert l.available()==[("A","Maps"),("B","Birds")]\nassert l.borrow("A")=="Maps" and l.available()==[("B","Birds")]\nassert l.give_back("A")=="Maps" and len(l.available())==2'),
         ('Reject invalid transitions and preserve state', '''
          source={"x":"One"}; l=Library(source); source["y"]="Two"
          assert l.borrow("x")=="One"
          for action,error in [(lambda:l.borrow("x"),ValueError),(lambda:l.borrow("missing"),KeyError),(lambda:l.give_back("missing"),KeyError)]:
              try: action()
              except error: pass
              else: raise AssertionError("Expected rejection")
          assert l.available()==[]
          l.give_back("x")
          try: l.give_back("x")
          except ValueError: pass
          else: raise AssertionError("Expected rejection")
          result=l.available(); result.clear()
          assert l.available()==[("x","One")] and Library({}).available()==[]
          ''')],
        ['Keep the catalog separate from the set of borrowed IDs.', 'Look up the ID before checking loan state.', 'Build a fresh sorted result when reporting availability.'],
        'Explicit transitions make the model predictable even when callers repeat requests or provide unknown IDs.',
        kind='project', minutes=40)
