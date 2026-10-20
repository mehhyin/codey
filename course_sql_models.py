"""SQL analysis and small predictive models using existing browser packages."""

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, date TEXT, amount REAL);
"""
SETUP = f"""
import sqlite3
connection=sqlite3.connect("analysis.db")
connection.executescript({SCHEMA!r})
connection.executemany("INSERT INTO customers VALUES (?,?)",[(1,"Aya"),(2,"Ben"),(3,"Cleo"),(4,"Dev")])
connection.executemany("INSERT INTO orders VALUES (?,?,?,?)",[
    (1,1,"2025-01-01",10),(2,1,"2025-01-03",30),(3,2,"2025-01-03",60),
    (4,3,"2025-02-01",20),(5,2,"2025-02-05",40)])
connection.commit()
connection.close()
"""
RESOURCE = {
    'name': 'analysis.db',
    'description': 'SQLite tables: `customers(customer_id INTEGER PRIMARY KEY, name TEXT)` and `orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, date TEXT, amount REAL)`. Each order belongs to a customer. Dates are valid `YYYY-MM-DD` strings; amounts are finite and nonnegative.',
    'preview': 'customers\ncustomer_id | name\n1 | Aya\n2 | Ben\n3 | Cleo\n4 | Dev\n\norders\norder_id | customer_id | date       | amount\n1        | 1           | 2025-01-01 | 10\n2        | 1           | 2025-01-03 | 30\n3        | 2           | 2025-01-03 | 60\n4        | 3           | 2025-02-01 | 20\n5        | 2           | 2025-02-05 | 40',
}


def extend_sql_models(section, unit):
    m = section('querylab', 'SQL for analytical questions',
        'Use conditional groups, common table expressions and window functions.',
        'Export a complete customer-value report', 'analytics', [
            ('Conditional values', 'SELECT CASE WHEN amount < 10 THEN \'low\' ELSE \'high\' END AS band FROM orders;',
             'CASE produces a value per row. Aggregate those values to summarize categories.'),
            ('Window calculations', 'SELECT order_id, SUM(amount) OVER (ORDER BY date, order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) FROM orders;',
             'A window calculation keeps individual rows. Explicit ordering resolves ties.'),
            ('Common table expressions', 'WITH totals AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id) SELECT * FROM totals;',
             'A CTE names an intermediate query so later calculations can refer to its columns.')
        ], ['sql-select', 'sql-parameters'])

    def sql_unit(*args, **kwargs):
        t = unit(m, *args, setup=SETUP, **kwargs)
        t['provided_resources'] = [RESOURCE]
        return t

    sql_unit('bands', 'Group orders into value bands',
        'Conditional aggregation can turn numeric observations into useful reporting categories. Define boundaries carefully so every valid amount belongs to exactly one band. In these exercises, functions receive an open SQLite connection; callers own it, so your function should not close it.',
        'def order_kinds(conn):\n    return conn.execute("SELECT CASE WHEN amount = 0 THEN \'free\' ELSE \'paid\' END FROM orders").fetchall()',
        ['Define `basket_bands(conn)` for a SQLite connection with the tables described above. Use SQL to compute the result.',
         'Classify amounts below 20 as `small`, amounts from 20 up to but excluding 50 as `medium`, and amounts of 50 or more as `large`.',
         'Return a list of `(band, order_count, total_amount)` tuples, sorted alphabetically by band. Include only bands with orders. For no orders return `[]`. Leave the connection open.'],
        '''
        def basket_bands(conn):
            return conn.execute("""
                SELECT CASE WHEN amount<20 THEN 'small' WHEN amount<50 THEN 'medium' ELSE 'large' END AS band,
                       COUNT(*), SUM(amount)
                FROM orders GROUP BY band ORDER BY band
            """).fetchall()
        ''',
        [('Summarise the provided orders', '''
          import sqlite3
          c=sqlite3.connect("analysis.db")
          assert basket_bands(c)==[("large",1,60),("medium",3,90),("small",1,10)]
          c.execute("SELECT 1"); c.close()
          '''),
         ('Honor boundaries on a different dataset', '''
          import sqlite3
          c=sqlite3.connect(":memory:"); c.execute("CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, date TEXT, amount REAL)")
          c.executemany("INSERT INTO orders VALUES (?,1,'2025-01-01',?)",[(1,0),(2,19.5),(3,20),(4,49),(5,50)])
          assert basket_bands(c)==[("large",1,50),("medium",2,69),("small",2,19.5)]
          c.execute("DELETE FROM orders"); assert basket_bands(c)==[]; c.close()
          ''')],
        ['Use CASE to assign one label to each row.', 'Group on that label and calculate both count and sum.', 'ORDER BY makes result order explicit.'],
        'Precise category boundaries make an aggregate interpretable and prevent gaps or double counting.')
    sql_unit('having', 'Filter customers after aggregation',
        'WHERE filters individual records before grouping; HAVING filters grouped results. A customer may qualify based on several small orders even if no individual order reaches the threshold. Use a bound SQL parameter for the threshold rather than inserting text into a query.',
        'def frequent_buyers(conn, threshold):\n    return conn.execute("SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id HAVING COUNT(*) >= ?", (threshold,)).fetchall()',
        ['Define `customer_totals(conn, minimum)`. `minimum` is a nonnegative numeric threshold.',
         'Use SQL to return `(customer_id, total_amount)` tuples for customers whose combined order amount is at least `minimum`. Include only customers with orders.',
         'Sort by total descending, then customer ID ascending for ties. Bind the threshold as a parameter and leave the connection open.'],
        '''
        def customer_totals(conn,minimum):
            return conn.execute("""
                SELECT customer_id,SUM(amount) AS total FROM orders
                GROUP BY customer_id HAVING SUM(amount)>=?
                ORDER BY total DESC,customer_id
            """,(minimum,)).fetchall()
        ''',
        [('Filter totals rather than individual orders', '''
          import sqlite3
          c=sqlite3.connect("analysis.db")
          assert customer_totals(c,40)==[(2,100),(1,40)] and customer_totals(c,101)==[]
          c.close()
          '''),
         ('Respect exact thresholds and tied totals', '''
          import sqlite3
          c=sqlite3.connect(":memory:"); c.execute("CREATE TABLE orders(customer_id INTEGER, amount REAL)")
          c.executemany("INSERT INTO orders VALUES (?,?)",[(3,8),(1,4),(1,4),(9,0)])
          assert customer_totals(c,8)==[(1,8),(3,8)]
          assert customer_totals(c,0)==[(1,8),(3,8),(9,0)]; c.close()
          ''')],
        ['Group orders before testing the total.', 'HAVING can compare the sum with a placeholder.', 'Add a second ORDER BY expression for ties.'],
        'Choosing the stage at which a filter applies changes the analytical question.')
    sql_unit('shares', 'Calculate shares from a grouped query',
        'A common table expression can name grouped totals before a second query calculates their share of the whole. SQLite may perform integer division when both operands are integers, so make the percentage calculation explicitly floating point. A zero grand total needs a defined result.',
        'def order_counts(conn):\n    query = """WITH counts AS (\n      SELECT customer_id, COUNT(*) AS n\n      FROM orders GROUP BY customer_id)\n    SELECT customer_id, n FROM counts"""\n    return conn.execute(query).fetchall()',
        ['Define `revenue_shares(conn)`, using a SQL common table expression to aggregate order amounts by customer.',
         'Return `(customer_id, percent)` tuples sorted by customer ID, for customers with orders. `percent` is each customer’s total divided by the grand total, multiplied by 100.',
         'Do not round. If the grand total is zero, return zero for every represented customer; return `[]` for no orders. Leave the connection open.'],
        '''
        def revenue_shares(conn):
            return conn.execute("""
                WITH totals AS (SELECT customer_id,SUM(amount) AS total FROM orders GROUP BY customer_id)
                SELECT customer_id,CASE WHEN (SELECT SUM(total) FROM totals)=0 THEN 0.0
                    ELSE 100.0*total/(SELECT SUM(total) FROM totals) END
                FROM totals ORDER BY customer_id
            """).fetchall()
        ''',
        [('Calculate shares from total revenue', '''
          import sqlite3
          c=sqlite3.connect("analysis.db")
          assert revenue_shares(c)==[(1,25),(2,62.5),(3,12.5)]; c.close()
          '''),
         ('Avoid integer truncation and handle zero revenue', '''
          import sqlite3
          c=sqlite3.connect(":memory:"); c.execute("CREATE TABLE orders(customer_id INTEGER,amount INTEGER)")
          c.executemany("INSERT INTO orders VALUES (?,?)",[(1,1),(2,2)])
          result=revenue_shares(c); assert abs(result[0][1]-100/3)<1e-10 and abs(result[1][1]-200/3)<1e-10
          c.execute("UPDATE orders SET amount=0"); assert revenue_shares(c)==[(1,0),(2,0)]
          c.execute("DELETE FROM orders"); assert revenue_shares(c)==[]; c.close()
          ''')],
        ['Name the per-customer totals in a WITH clause.', 'Calculate the grand total from that grouped result.', 'Use a CASE for zero and 100.0 for floating-point division.'],
        'Separating aggregation from normalization makes the denominator visible.')
    sql_unit('running', 'Keep rows while computing running totals',
        'Window functions attach a calculation to each row without collapsing the dataset. A running total needs a deterministic order, especially when multiple orders occur on the same date. A ROWS frame advances one row at a time rather than combining rows with tied ordering values.',
        'def numbered_orders(conn):\n    query = "SELECT order_id, ROW_NUMBER() OVER (ORDER BY date, order_id) FROM orders"\n    return conn.execute(query).fetchall()',
        ['Define `running_revenue(conn)` using a SQL window function.',
         'Return `(order_id, running_total)` tuples in ascending date order, breaking same-date ties by ascending order ID.',
         'Each total includes that order and every preceding order in this ordering. Return `[]` for no orders and leave the connection open.'],
        '''
        def running_revenue(conn):
            return conn.execute("""
                SELECT order_id,SUM(amount) OVER (ORDER BY date,order_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                FROM orders ORDER BY date,order_id
            """).fetchall()
        ''',
        [('Accumulate without collapsing same-day orders', '''
          import sqlite3
          c=sqlite3.connect("analysis.db")
          assert running_revenue(c)==[(1,10),(2,40),(3,100),(4,120),(5,160)]; c.close()
          '''),
         ('Order by date and ID, not insertion order', '''
          import sqlite3
          c=sqlite3.connect(":memory:"); c.execute("CREATE TABLE orders(order_id INTEGER,date TEXT,amount REAL)")
          c.executemany("INSERT INTO orders VALUES (?,?,?)",[(3,"2025-02-01",9),(2,"2025-01-01",4),(1,"2025-01-01",2)])
          assert running_revenue(c)==[(1,2),(2,6),(3,15)]
          c.execute("DELETE FROM orders"); assert running_revenue(c)==[]; c.close()
          ''')],
        ['Put the same ordering inside and outside the OVER clause.', 'Use a ROWS frame from the beginning through the current row.', 'Keep order_id in the result so each total can be traced to an order.'],
        'Window calculations preserve detail while adding a cumulative view.')
    sql_unit('rank', 'Rank spending while keeping ties',
        'Dense ranking assigns equal ranks to equal values and does not leave gaps after ties. Rank total customer spending, rather than individual orders. A separate output sort provides stable ordering among customers sharing a rank.',
        'def rank_orders(conn):\n    query = "SELECT order_id, DENSE_RANK() OVER (ORDER BY amount DESC) FROM orders"\n    return conn.execute(query).fetchall()',
        ['Define `spending_ranks(conn)` using SQL aggregation and `DENSE_RANK()`.',
         'Return `(customer_id, total_amount, rank)` tuples for customers with orders. The highest total has rank 1; equal totals share a rank and the next distinct total receives the next integer.',
         'Sort by rank ascending, then customer ID ascending. Return `[]` for no orders; leave the connection open.'],
        '''
        def spending_ranks(conn):
            return conn.execute("""
                WITH totals AS (SELECT customer_id,SUM(amount) AS total FROM orders GROUP BY customer_id)
                SELECT customer_id,total,DENSE_RANK() OVER (ORDER BY total DESC) AS position
                FROM totals ORDER BY position,customer_id
            """).fetchall()
        ''',
        [('Rank aggregated totals', '''
          import sqlite3
          c=sqlite3.connect("analysis.db")
          assert spending_ranks(c)==[(2,100,1),(1,40,2),(3,20,3)]; c.close()
          '''),
         ('Keep ties without gaps', '''
          import sqlite3
          c=sqlite3.connect(":memory:"); c.execute("CREATE TABLE orders(customer_id INTEGER,amount REAL)")
          c.executemany("INSERT INTO orders VALUES (?,?)",[(3,10),(1,5),(1,5),(2,4)])
          assert spending_ranks(c)==[(1,10,1),(3,10,1),(2,4,2)]
          c.execute("DELETE FROM orders"); assert spending_ranks(c)==[]; c.close()
          ''')],
        ['Aggregate into one row per customer first.', 'Rank by total only so equal totals remain tied.', 'Use customer ID only for the final presentation order.'],
        'Separating rank criteria from display ordering preserves the intended meaning of a tie.')
    sql_unit('customer-project', 'Project · export customer value',
        'A customer report should include people who have never ordered. A left join and correct counting preserve those zero-activity customers. The exported report must use a consistent population for counts, revenue totals and revenue shares.',
        'def order_counts(conn):\n    query = """SELECT c.customer_id, COUNT(o.order_id)\n    FROM customers c LEFT JOIN orders o\n    ON c.customer_id=o.customer_id\n    GROUP BY c.customer_id"""\n    return conn.execute(query).fetchall()',
        ['Connect to `analysis.db`. Create `customers.csv` with columns `customer_id`, `name`, `order_count`, `revenue`, `share_percent`, sorted by revenue descending then customer ID ascending.',
         'Include every customer, including those without orders. Use zero for their count, revenue and share. Calculate share against all order revenue, rounded to two decimals.',
         'Write `customer_audit.json` with `customers` (all customer count), `active_customers` (customers with at least one order), and `total_revenue`.',
         'Use SQL to aggregate customer activity. Close the connection after writing the files.'],
        '''
        import sqlite3,csv,json
        conn=sqlite3.connect("analysis.db")
        rows=conn.execute("""
            WITH summary AS (
              SELECT c.customer_id,c.name,COUNT(o.order_id) AS order_count,COALESCE(SUM(o.amount),0) AS revenue
              FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id GROUP BY c.customer_id,c.name
            )
            SELECT customer_id,name,order_count,revenue,
              CASE WHEN (SELECT SUM(revenue) FROM summary)=0 THEN 0.0
                   ELSE ROUND(100.0*revenue/(SELECT SUM(revenue) FROM summary),2) END
            FROM summary ORDER BY revenue DESC,customer_id
        """).fetchall()
        with open("customers.csv","w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow(["customer_id","name","order_count","revenue","share_percent"])
            writer.writerows(rows)
        with open("customer_audit.json","w") as f:
            json.dump({"customers":len(rows),"active_customers":sum(r[2]>0 for r in rows),"total_revenue":sum(r[3] for r in rows)},f)
        conn.close()
        ''',
        [('Include inactive customers and correct shares', '''
          import pandas as pd
          result=pd.read_csv("customers.csv")
          assert list(result.columns)==["customer_id","name","order_count","revenue","share_percent"]
          assert result.to_dict("list")=={"customer_id":[2,1,3,4],"name":["Ben","Aya","Cleo","Dev"],"order_count":[2,2,1,0],"revenue":[100,40,20,0],"share_percent":[62.5,25,12.5,0]}
          '''),
         ('Reconcile the audit with the report', '''
          import json
          with open("customer_audit.json") as f:
              assert json.load(f)=={"customers":4,"active_customers":3,"total_revenue":160}
          ''')],
        ['Count matched order IDs, not all joined rows.', 'COALESCE can replace a missing revenue sum with zero.', 'Use the same grouped result for the CSV and audit.'],
        'Including inactive customers makes the reporting population explicit and prevents overstating engagement.',
        exports=['customers.csv','customer_audit.json'],kind='project',minutes=40)

    m = section('modeling', 'Build and evaluate simple models',
        'Learn baselines, leakage prevention and honest evaluation.',
        'Compare a demand model with a baseline', 'analytics', [
            ('Train and evaluate separately', 'train = rows[:cutoff]\ntest = rows[cutoff:]',
             'Holdout data estimates performance on unseen observations. Time-ordered data should not leak later observations into earlier training.'),
            ('Training-only scaling', 'scaled = (values - training_mean) / training_std',
             'Learn preprocessing statistics on training data, then reuse them for the holdout.'),
            ('Prediction error', 'mae = sum(abs(y-p) for y,p in zip(actual,predicted)) / len(actual)',
             'Mean absolute error uses the target’s units. Compare it with a simple baseline before calling a model useful.')
        ], ['arrays-vector', 'analysis-spread', 'charts-line'])
    unit(m, 'split', 'Hold out the latest observations',
        'Random splitting is not always appropriate for time-ordered data. If you predict future demand, learning from later observations can leak information into training. This exercise assumes records are already in chronological order and makes the holdout boundary explicit.',
        'observations = [4,6,5,8]\nearly = observations[:2]\nlate = observations[2:]',
        ['Define `time_split(rows, test_size)` where `rows` is a list in chronological order and `test_size` is an integer.',
         'Return `(train, test)` as two new lists: training contains all but the final `test_size` records, and test contains those final records in their original order.',
         'Require `1 <= test_size < len(rows)`; otherwise raise `ValueError`. Do not modify the input. Shallow list copies are sufficient.'],
        '''
        def time_split(rows,test_size):
            if not 1 <= test_size < len(rows):
                raise ValueError("Need nonempty train and test sets")
            return rows[:-test_size],rows[-test_size:]
        ''',
        [('Retain chronological order', 'rows=[5,2,9,1]; train,test=time_split(rows,2)\nassert train==[5,2] and test==[9,1]\ntrain.append(0); test.clear(); assert rows==[5,2,9,1]'),
         ('Reject empty training or test sets', '''
          for rows,size in [([],1),([1],1),([1,2],0),([1,2],2),([1,2],-1)]:
              try: time_split(rows,size)
              except ValueError: pass
              else: raise AssertionError("Invalid split accepted")
          ''')],
        ['Work out the boundary from the end of the list.', 'Both returned datasets must contain at least one record.', 'List slices produce new outer lists.'],
        'A chronological holdout more closely reflects predicting later data from earlier observations.')
    unit(m, 'scale', 'Fit preprocessing on training data only',
        'Standardization can leak information if its mean and standard deviation use the holdout set. Learn both statistics from the training values, then apply the same transformation to training and test values. A constant training feature uses a scale of one here, preserving distances from its training mean.',
        'training_mean = sum(training_values) / len(training_values)\n# Test values must not influence training_mean.',
        ['Define `scale_feature(train, test)` for finite numeric lists; `train` is nonempty and `test` may be empty.',
         'Calculate the training mean and population standard deviation. Use scale 1 when that standard deviation is zero.',
         'Return `(scaled_train, scaled_test)` as lists, using those same training statistics for both. Do not round or modify either input.'],
        '''
        import math
        def scale_feature(train,test):
            mean=sum(train)/len(train)
            scale=math.sqrt(sum((x-mean)**2 for x in train)/len(train)) or 1
            return [(x-mean)/scale for x in train],[(x-mean)/scale for x in test]
        ''',
        [('Exclude the holdout from fitted statistics', '''
          import numpy as np
          train=[0,2]; test=[100]
          a,b=scale_feature(train,test)
          assert np.allclose(a,[-1,1]) and np.allclose(b,[99])
          assert train==[0,2] and test==[100]
          '''),
         ('Use the constant-feature convention', 'assert scale_feature([3,3],[3,5])==([0,0],[0,2])\nassert scale_feature([4],[])==([0],[])')],
        ['Compute the mean and spread once, from train.', 'Use the same scale for both output lists.', 'A constant feature should not cause division by zero.'],
        'Keeping preprocessing inside the training boundary prevents a subtle form of evaluation leakage.')
    unit(m, 'line', 'Fit a one-feature regression',
        'A straight-line regression predicts y as slope×x + intercept. Least squares chooses coefficients that minimize squared residuals. For one feature, slope is the sum of paired deviations divided by the sum of squared x deviations; intercept is mean(y) − slope×mean(x). A constant feature cannot identify a slope, so use slope zero and the target mean.',
        'prediction = slope * feature + intercept\nresidual = observed - prediction',
        ['Define `fit_line(x, y)` for nonempty, equally sized lists of finite numbers.',
         'Return `(slope, intercept)` for ordinary least-squares regression with an intercept, using the formula described above. Do not round.',
         'When all x values are identical, return slope zero and intercept equal to the mean of y. Leave both lists unchanged.'],
        '''
        def fit_line(x,y):
            mx=sum(x)/len(x); my=sum(y)/len(y)
            denominator=sum((v-mx)**2 for v in x)
            slope=sum((a-mx)*(b-my) for a,b in zip(x,y))/denominator if denominator else 0.0
            return slope,my-slope*mx
        ''',
        [('Fit positive and negative relationships', '''
          import numpy as np
          assert np.allclose(fit_line([0,1,2],[1,3,5]),(2,1))
          assert np.allclose(fit_line([1,2,3],[8,5,2]),(-3,11))
          '''),
         ('Handle noisy and constant features', '''
          import numpy as np
          x=[0,1,2]; y=[0,1,3]
          assert np.allclose(fit_line(x,y),(1.5,-1/6))
          assert x==[0,1,2] and y==[0,1,3]
          assert fit_line([2,2],[4,8])==(0,6) and fit_line([1],[9])==(0,9)
          ''')],
        ['Center both variables around their own means.', 'The denominator depends only on x.', 'After finding the slope, solve for the intercept from the two means.'],
        'A fitted relationship describes association in the supplied data; it does not by itself establish causation.')
    unit(m, 'metrics', 'Evaluate a binary classifier',
        'Accuracy can look high when one class is rare. Precision asks how often positive predictions are correct; recall asks how many actual positives were found. Defining the positive class and the zero-denominator convention prevents ambiguous metrics.',
        'true_positive = actual == 1 and predicted == 1\nfalse_positive = actual == 0 and predicted == 1',
        ['Define `binary_metrics(actual, predicted)` for equally sized nonempty lists containing only 0 or 1. Class 1 is positive.',
         'Return exactly `accuracy`, `precision`, and `recall` as fractions from 0 to 1, without rounding.',
         'Accuracy is correct predictions / all predictions; precision is true positives / predicted positives; recall is true positives / actual positives. Use zero for precision or recall when its denominator is zero.'],
        '''
        def binary_metrics(actual,predicted):
            tp=sum(a==1 and p==1 for a,p in zip(actual,predicted))
            pp=sum(predicted); ap=sum(actual)
            return {"accuracy":sum(a==p for a,p in zip(actual,predicted))/len(actual),
                    "precision":tp/pp if pp else 0.0,"recall":tp/ap if ap else 0.0}
        ''',
        [('Use different precision and recall denominators', '''
          r=binary_metrics([1,1,0,0],[1,0,1,1])
          assert set(r)=={"accuracy","precision","recall"}
          assert r["accuracy"]==0.25 and abs(r["precision"]-1/3)<1e-12 and r["recall"]==0.5
          '''),
         ('Handle absent positive classes', 'assert binary_metrics([0,0],[0,0])=={"accuracy":1,"precision":0,"recall":0}\nassert binary_metrics([1,1],[0,0])=={"accuracy":0,"precision":0,"recall":0}')],
        ['Count true positives before calculating the rates.', 'The two positive counts refer to different lists.', 'Keep fractions numeric rather than formatting percentage strings.'],
        'Different error types matter in different applications; one score rarely tells the full story.')
    unit(m, 'neighbor', 'Predict with the nearest observation',
        'A nearest-neighbor model predicts from the most similar training observation. Euclidean distance combines feature differences; squared distance gives the same ordering without a square root. Features should be on comparable scales. A tie-breaking rule is needed for reproducibility.',
        'a = [1,4]\nb = [3,7]\nsquared_distance = sum((x-y)**2 for x,y in zip(a,b))',
        ['Define `nearest_label(points, labels, query)`. `points` is a nonempty list of numeric feature lists; `labels` has one label per point. All points and `query` have the same positive dimension.',
         'Return the label of the point with the smallest Euclidean distance to `query`.',
         'On an exact distance tie, choose the earliest point in the input. Do not modify the data.'],
        '''
        def nearest_label(points,labels,query):
            index=min(range(len(points)),key=lambda i:sum((a-b)**2 for a,b in zip(points[i],query)))
            return labels[index]
        ''',
        [('Compare all feature dimensions', 'assert nearest_label([[0,0],[0,9],[6,6]],["A","B","C"],[0,8])=="B"\nassert nearest_label([[1],[8]],["near","far"],[2])=="near"'),
         ('Resolve ties by input position', 'points=[[0,0],[2,0]]; labels=["first","second"]\nassert nearest_label(points,labels,[1,0])=="first"\nassert points==[[0,0],[2,0]] and labels==["first","second"]')],
        ['Compute a distance for every training point.', 'Track the index so the matching label can be returned.', 'Update only for a strictly smaller distance to preserve the earliest tie.'],
        'Even a simple model needs a defined distance, feature scaling policy and tie behavior.')
    unit(m, 'demand-project', 'Project · compare a model with a baseline',
        'A fictional kiosk wants to predict daily cup demand from temperature. Use the first four dated records for training and the final two for evaluation. Compare a fitted straight line against a baseline that always predicts mean training demand. The holdout is deliberately small; this is a workflow demonstration rather than evidence of dependable forecasting.',
        'errors = [abs(a-p) for a,p in zip(actual,predicted)]\nmae = sum(errors) / len(errors)',
        ['Read `demand.csv` in its given chronological order. Train on its first four rows and evaluate on its final two rows. Use `temperature` as the feature and `cups` as the target.',
         'Fit a least-squares line with an intercept using training data only. The baseline always predicts the mean training cups. Predict both held-out rows with each approach.',
         'Write `predictions.csv` with `date`, `actual`, `model`, `baseline` for the held-out rows in order.',
         'Write `evaluation.json` with `model_mae`, `baseline_mae`, and `winner`. Winner is `"model"` if its MAE is lower by more than `1e-12`, `"baseline"` for the reverse, and `"tie"` otherwise. Do not round numeric outputs.',
         'Create a chart named `ax` with three labeled lines: actual, model and baseline cups across the held-out dates. Add a title, axis labels and legend; save `holdout.png`.'],
        '''
        import csv,json
        import matplotlib.pyplot as plt
        with open("demand.csv",newline="") as f: rows=list(csv.DictReader(f))
        train=rows[:4]; test=rows[4:]
        x=[float(r["temperature"]) for r in train]; y=[float(r["cups"]) for r in train]
        mx=sum(x)/len(x); my=sum(y)/len(y)
        slope=sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)
        intercept=my-slope*mx
        dates=[r["date"] for r in test]
        actual=[float(r["cups"]) for r in test]
        predictions=[slope*float(r["temperature"])+intercept for r in test]
        baseline=[my]*len(test)
        with open("predictions.csv","w",newline="") as f:
            w=csv.writer(f); w.writerow(["date","actual","model","baseline"])
            w.writerows(zip(dates,actual,predictions,baseline))
        model_mae=sum(abs(a-p) for a,p in zip(actual,predictions))/len(test)
        baseline_mae=sum(abs(a-p) for a,p in zip(actual,baseline))/len(test)
        winner="model" if model_mae<baseline_mae-1e-12 else "baseline" if baseline_mae<model_mae-1e-12 else "tie"
        with open("evaluation.json","w") as f:
            json.dump({"model_mae":model_mae,"baseline_mae":baseline_mae,"winner":winner},f)
        fig,ax=plt.subplots()
        for values,label in [(actual,"actual"),(predictions,"model"),(baseline,"baseline")]:
            ax.plot(dates,values,marker="o",label=label)
        ax.set(title="Held-out cup demand",xlabel="Date",ylabel="Cups"); ax.legend()
        fig.savefig("holdout.png")
        ''',
        [('Keep evaluation data out of fitting', '''
          import pandas as pd,json
          r=pd.read_csv("predictions.csv")
          assert list(r.columns)==["date","actual","model","baseline"]
          assert r.to_dict("list")=={"date":["2025-06-05","2025-06-06"],"actual":[17,30],"model":[18,20],"baseline":[13,13]}
          with open("evaluation.json") as f: e=json.load(f)
          assert e=={"model_mae":5.5,"baseline_mae":10.5,"winner":"model"}
          '''),
         ('Plot held-out predictions and the baseline', '''
          from pathlib import Path
          series={line.get_label():list(line.get_ydata()) for line in ax.lines}
          assert series=={"actual":[17,30],"model":[18,20],"baseline":[13,13]}
          assert all(list(line.get_xdata())==["2025-06-05","2025-06-06"] for line in ax.lines)
          assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel() and ax.get_legend() is not None
          assert Path("holdout.png").read_bytes().startswith(b"\\x89PNG")
          ''')],
        ['Fit both model coefficients and baseline mean on the first four rows only.', 'Use the same held-out observations for both MAEs.', 'Keep dates alongside predictions so exports and charts can be reconciled.'],
        'The model beats this baseline on this holdout, but two test observations are too few to claim reliable generalization.',
        files={'demand.csv':'date,temperature,cups\n2025-06-01,10,10\n2025-06-02,12,12\n2025-06-03,14,14\n2025-06-04,16,16\n2025-06-05,18,17\n2025-06-06,20,30\n'},
        exports=['predictions.csv','evaluation.json','holdout.png'],kind='project',minutes=45)
