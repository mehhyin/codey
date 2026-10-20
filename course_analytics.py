"""Original analysis exercises with explicit data and output contracts."""


def extend_analytics(section, unit):
    m = section('explore', 'Investigate and prepare data',
        'Ask what each row means before calculating a headline.',
        'Investigate service response times', 'analytics', [
            ('Missingness', 'missing = frame.isna().sum()\npercent = frame.isna().mean() * 100',
             'Count missing values per column. A missing observation is not automatically a zero.'),
            ('Join validation', 'joined = orders.merge(customers, on="customer_id", validate="many_to_one")',
             'A duplicated lookup key can multiply rows and inflate totals. Validate the intended relationship.'),
            ('Dates and months', 'dates = pd.to_datetime(frame["date"], errors="coerce")\nmonths = dates.dt.to_period("M")',
             'Invalid dates become NaT. Periods group all days of the same month together.')
        ], ['pandas-table', 'analysis-missing'])
    unit(m, 'profile', 'Measure missingness by column',
        'An initial data audit should describe both dataset size and incomplete fields. pandas isna recognizes missing cells such as None and NaN. An empty string is not missing unless you explicitly decide to treat it that way. Percentages use the number of rows as their denominator.',
        'import pandas as pd\nsample = pd.DataFrame({"cost": [5, None]})\nmissing = sample["cost"].isna().sum()',
        ['Define `missing_profile(df)` for a pandas DataFrame. Return a new DataFrame with columns `missing` (count) and `percent` (0–100), indexed by the original column names in their original order.',
         'Treat only pandas-recognized missing values as missing. Round percentages to one decimal place.',
         'For a DataFrame with no rows, report zero counts and percentages for every column. Do not modify the input.'],
        '''
        import pandas as pd
        def missing_profile(df):
            counts=df.isna().sum()
            percents=(counts/len(df)*100).round(1) if len(df) else counts.astype(float)
            return pd.DataFrame({"missing":counts,"percent":percents})
        ''',
        [('Measure each column in order', '''
          import pandas as pd
          frame=pd.DataFrame({"b":[1,None,3],"a":[None,"",None]})
          original=frame.copy(deep=True); result=missing_profile(frame)
          assert list(result.index)==["b","a"] and list(result.columns)==["missing","percent"]
          assert result["missing"].tolist()==[1,2] and result["percent"].tolist()==[33.3,66.7]
          pd.testing.assert_frame_equal(frame,original)
          '''),
         ('Handle empty and complete datasets', '''
          import pandas as pd
          result=missing_profile(pd.DataFrame(columns=["x","y"]))
          assert result["missing"].tolist()==[0,0] and result["percent"].tolist()==[0,0]
          assert missing_profile(pd.DataFrame({"x":[0,""]}))["missing"].iloc[0]==0
          ''')],
        ['Compute a missing-value mask first.', 'Reduce the mask down the rows to get one count per column.', 'Handle zero rows before dividing.'],
        'A missingness profile shows which fields need investigation without inventing replacement values.')
    unit(m, 'categories', 'Normalize survey categories',
        'Category spelling can fragment a frequency table: extra spaces and different capitalization may describe the same answer. Normalization should follow a stated policy. Unknown responses should remain visible rather than being forced into a valid category.',
        'label = "  Weekend ".strip().lower()\nallowed = {"weekday", "weekend"}',
        ['Define `category_counts(values)` for an iterable of strings or `None`.',
         'Strip strings and lowercase them. Count `yes`, `no` and `maybe` as those categories; count blanks, `None` and every other string as `unknown`.',
         'Return a dictionary containing exactly `yes`, `no`, `maybe` and `unknown`, including zero counts. Empty input returns four zeros.'],
        '''
        def category_counts(values):
            counts=dict.fromkeys(["yes","no","maybe","unknown"],0)
            for value in values:
                label=value.strip().lower() if value is not None else ""
                counts[label if label in {"yes","no","maybe"} else "unknown"] += 1
            return counts
        ''',
        [('Normalize without dropping unknown answers', 'assert category_counts([" YES ","no","Maybe",None,"","y"])=={"yes":1,"no":1,"maybe":1,"unknown":3}'),
         ('Keep absent categories and accept iterators', 'assert category_counts(iter(["No","NO"]))=={"yes":0,"no":2,"maybe":0,"unknown":0}\nassert category_counts([])=={"yes":0,"no":0,"maybe":0,"unknown":0}')],
        ['Initialize all four keys before reading responses.', 'Do not call string methods on None.', 'Only the three specified labels count as known categories.'],
        'Explicit unknown counts reveal quality problems that a filtered frequency table would conceal.')
    unit(m, 'join', 'Guard against multiplying records',
        'A lookup table should have one row per key. A many-to-one join preserves the number of source records, even if several source records use the same key. An unmatched key should remain visible in a left join. A missing lookup label has a defined reporting replacement here.',
        'import pandas as pd\n# validate="many_to_one" rejects duplicate lookup keys.',
        ['Define `attach_region(orders, customers)` for two DataFrames. `orders` has `order_id` and `customer_id`; `customers` has `customer_id` and `region`. IDs are nonmissing integers.',
         'Return a new DataFrame containing `order_id`, `customer_id`, `region`, in that order. Preserve all order rows and their order; use a fresh default integer index.',
         'Use `"Unknown"` for unmatched customers or missing regions. Raise `ValueError` if any customer ID appears more than once in `customers`, even if its region is the same. Do not modify either input.'],
        '''
        def attach_region(orders,customers):
            if customers["customer_id"].duplicated().any():
                raise ValueError("Duplicate customer")
            result=orders.merge(customers,on="customer_id",how="left",sort=False,validate="many_to_one")
            result["region"]=result["region"].fillna("Unknown")
            return result[["order_id","customer_id","region"]].reset_index(drop=True)
        ''',
        [('Preserve orders and disclose unmatched keys', '''
          import pandas as pd
          orders=pd.DataFrame({"order_id":[9,2,5],"customer_id":[2,1,7]})
          customers=pd.DataFrame({"customer_id":[1,2],"region":["East",None]})
          a,b=orders.copy(),customers.copy()
          result=attach_region(orders,customers)
          assert list(result.columns)==["order_id","customer_id","region"]
          assert result.to_dict("records")==[{"order_id":9,"customer_id":2,"region":"Unknown"},{"order_id":2,"customer_id":1,"region":"East"},{"order_id":5,"customer_id":7,"region":"Unknown"}]
          assert result.index.tolist()==[0,1,2]
          pd.testing.assert_frame_equal(a,orders); pd.testing.assert_frame_equal(b,customers)
          '''),
         ('Reject duplicate lookup keys', '''
          import pandas as pd
          try: attach_region(pd.DataFrame({"order_id":[1],"customer_id":[2]}),pd.DataFrame({"customer_id":[2,2],"region":["A","A"]}))
          except ValueError: pass
          else: raise AssertionError("Duplicate lookup accepted")
          ''')],
        ['Validate customer IDs before joining.', 'A left join retains unmatched orders.', 'Fill the resulting region column, not the customer IDs.'],
        'Checking cardinality prevents a plausible-looking report from double-counting source records.')
    unit(m, 'months', 'Show months with no activity',
        'A chart can hide inactive periods when it includes only observed dates. A complete monthly index makes those gaps explicit. In this dataset an absent month means zero recorded sales, while an invalid date means the row cannot be assigned to a month.',
        'import pandas as pd\ncalendar = pd.period_range("2025-02","2025-04",freq="M")\n# A complete calendar includes the middle month.',
        ['Define `monthly_sales(df)`. `df` has `date` strings in `YYYY-MM-DD` format (possibly invalid) and finite numeric `amount` values.',
         'Discard rows with invalid or missing dates. Sum amounts by calendar month, including refunds as negative amounts.',
         'Return a dictionary whose `YYYY-MM` keys run from the earliest valid month to the latest in chronological insertion order. Include missing months with total zero. If no dates are valid, return `{}`. Leave `df` unchanged.'],
        '''
        import pandas as pd
        def monthly_sales(df):
            dates=pd.to_datetime(df["date"],format="%Y-%m-%d",errors="coerce")
            valid=dates.notna()
            if not valid.any():
                return {}
            totals=df.loc[valid,"amount"].groupby(dates[valid].dt.to_period("M")).sum()
            months=pd.period_range(totals.index.min(),totals.index.max(),freq="M")
            return {str(month):float(totals.get(month,0)) for month in months}
        ''',
        [('Fill gaps and retain refunds', '''
          import pandas as pd
          df=pd.DataFrame({"date":["2025-03-03","2025-01-01","bad","2025-03-08"],"amount":[10,4,999,-2]})
          old=df.copy(); result=monthly_sales(df)
          assert list(result)==["2025-01","2025-02","2025-03"] and list(result.values())==[4,0,8]
          pd.testing.assert_frame_equal(df,old)
          '''),
         ('Cross year boundaries and handle invalid dates', '''
          import pandas as pd
          assert monthly_sales(pd.DataFrame({"date":["2024-12-01","2025-02-01"],"amount":[2,3]}))=={"2024-12":2,"2025-01":0,"2025-02":3}
          assert monthly_sales(pd.DataFrame({"date":["bad",None],"amount":[1,2]}))=={}
          ''')],
        ['Parse dates with a defined format and errors="coerce".', 'Group valid observations by monthly periods.', 'Reindex against a complete monthly range.'],
        'A continuous calendar distinguishes no recorded activity from a missing point on a chart.')
    unit(m, 'iqr', 'Flag unusual observations',
        'The interquartile range (IQR) spans the middle half of a distribution: Q3 minus Q1. A common screening rule flags values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR. This is a flag for investigation, not evidence that a record is wrong. Quantile interpolation matters on small samples.',
        'import numpy as np\nq = np.quantile([2,4,6,8],0.5,method="linear")',
        ['Define `iqr_flags(values)` for a list of finite numbers.',
         'Compute Q1 and Q3 using NumPy quantiles at 0.25 and 0.75 with `method="linear"`. Apply the 1.5×IQR rule.',
         'Return a list of Booleans in input order, true only for values strictly outside the two fences. Values exactly on a fence are not flagged. Return `[]` for empty input.'],
        '''
        import numpy as np
        def iqr_flags(values):
            if not values:
                return []
            q1,q3=np.quantile(values,[0.25,0.75],method="linear")
            gap=q3-q1
            return [bool(x<q1-1.5*gap or x>q3+1.5*gap) for x in values]
        ''',
        [('Flag both tails without changing order', 'assert iqr_flags([0,10,11,12,13,100])==[True,False,False,False,False,True]'),
         ('Respect fences and degenerate samples', 'assert iqr_flags([0,0,0,2,5])==[False]*5\nassert iqr_flags([4,4,4,4,9])==[False,False,False,False,True]\nassert iqr_flags([])==[] and iqr_flags([7])==[False]')],
        ['Calculate both quartiles using the same interpolation rule.', 'Compute the fences before comparing individual observations.', 'A constant sample has an IQR of zero.'],
        'A reproducible flagging rule supports review without automatically deleting inconvenient observations.')
    unit(m, 'service-project', 'Project · explain service response times',
        'An operations team wants to compare response time by support channel. Cleaning rules and denominators belong in the report: invalid records must not affect averages, and a low average based on very few observations needs its count alongside it. Build a reproducible summary and chart from the supplied synthetic data.',
        'import pandas as pd\n# Group summaries can contain both a count and a median.',
        ['Read `tickets.csv`. Strip and lowercase `channel`. Accept only `chat` or `email` and a finite, nonnegative numeric `minutes`; reject other rows once each.',
         'Create `channel_report.csv` with columns `channel`, `count`, `mean_minutes`, `median_minutes`, sorted alphabetically by channel. Round both statistics to two decimals. Include only channels with accepted rows.',
         'Write `quality.json` containing integer `accepted` and `rejected` counts.',
         'Create a bar chart named `ax` of mean response minutes by channel, with channel labels, a descriptive title and labeled axes. Save it as `response_times.png`.'],
        '''
        import json
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        raw=pd.read_csv("tickets.csv")
        raw["channel"]=raw["channel"].str.strip().str.lower()
        raw["minutes"]=pd.to_numeric(raw["minutes"],errors="coerce")
        mask=raw["channel"].isin(["chat","email"]) & np.isfinite(raw["minutes"]) & raw["minutes"].ge(0)
        clean=raw.loc[mask]
        report=clean.groupby("channel")["minutes"].agg(count="count",mean_minutes="mean",median_minutes="median").round(2).reset_index()
        report.to_csv("channel_report.csv",index=False)
        with open("quality.json","w") as f:
            json.dump({"accepted":int(mask.sum()),"rejected":int((~mask).sum())},f)
        fig,ax=plt.subplots()
        ax.bar(report["channel"],report["mean_minutes"])
        ax.set(title="Mean response time by channel",xlabel="Channel",ylabel="Minutes")
        fig.savefig("response_times.png")
        ''',
        [('Clean and aggregate the supplied data', '''
          import pandas as pd, json
          r=pd.read_csv("channel_report.csv")
          assert list(r.columns)==["channel","count","mean_minutes","median_minutes"]
          assert r.to_dict("list")=={"channel":["chat","email"],"count":[3,3],"mean_minutes":[4.0,20.0],"median_minutes":[4.0,15.0]}
          with open("quality.json") as f: assert json.load(f)=={"accepted":6,"rejected":4}
          '''),
         ('Chart the same means with readable labels', '''
          from pathlib import Path
          assert [p.get_height() for p in ax.patches]==[4,20]
          assert [t.get_text() for t in ax.get_xticklabels()]==["chat","email"]
          assert ax.get_title() and ax.get_xlabel() and ax.get_ylabel()
          assert Path("response_times.png").read_bytes().startswith(b"\\x89PNG")
          ''')],
        ['Convert invalid numeric text to missing values, then check finiteness and range.', 'Compute all channel statistics from the same accepted records.', 'Build the chart from the exported summary so the two outputs agree.'],
        'The mean, median, counts and rejection audit provide context for comparing channels. This observational report does not explain why they differ.',
        files={'tickets.csv':'ticket_id,channel,minutes\n1, Chat ,2\n2,chat,4\n3,CHAT,6\n4,email,5\n5,email,15\n6,Email,40\n7,phone,10\n8,chat,-1\n9,email,unknown\n10,chat,inf\n'},
        exports=['channel_report.csv','quality.json','response_times.png'],kind='project',minutes=40)

    m = section('inference', 'Probability, sampling and evidence',
        'Distinguish an observed difference from evidence for a conclusion.',
        'Audit a small randomized experiment', 'analytics', [
            ('Conditional probability', 'probability = joint_count / condition_count',
             'Conditioning restricts the denominator to observations meeting the condition.'),
            ('Standard scores', 'z = (value - mean) / standard_deviation',
             'A z-score measures distance from a mean in standard deviation units.'),
            ('Resampling', 'sample = [values[i] for i in indices]',
             'Bootstrap samples reuse observations with replacement. A permutation test reallocates the pooled observations under an exchangeability assumption.')
        ], ['analysis-proportions', 'analysis-spread', 'functions-return'])
    unit(m, 'conditional', 'Choose the probability denominator',
        'Conditional probability asks about a restricted population. P(renewed | contacted) counts renewed customers among contacted customers only, rather than among everyone. When nobody meets the condition, this empirical rate is undefined.',
        'subgroup = [row for row in records if row["eligible"]]\n# Rates for this subgroup use its size as the denominator.',
        ['Define `renewal_probability(records)`. Each record has Boolean fields `contacted` and `renewed`.',
         'Return the fraction of contacted customers who renewed, as a number from 0 to 1. Do not round or multiply by 100.',
         'Return `None` if no customers were contacted, including for empty input. Do not change the records.'],
        '''
        def renewal_probability(records):
            selected=[r for r in records if r["contacted"]]
            return sum(r["renewed"] for r in selected)/len(selected) if selected else None
        ''',
        [('Use only the conditioned population', 'assert renewal_probability([{"contacted":True,"renewed":True},{"contacted":True,"renewed":False},{"contacted":False,"renewed":True}])==0.5'),
         ('Distinguish zero from undefined', 'assert renewal_probability([{"contacted":True,"renewed":False}])==0\nassert renewal_probability([{"contacted":False,"renewed":True}]) is None\nassert renewal_probability([]) is None')],
        ['Count contacted customers separately from all customers.', 'The numerator requires both conditions.', 'Check the denominator before dividing.'],
        'The denominator defines the meaning of a probability. An undefined rate is different from zero.')
    unit(m, 'standard-scores', 'Compare values on a common scale',
        'A z-score expresses an observation relative to its group’s mean and standard deviation. This exercise uses the population standard deviation: divide the sum of squared deviations by N. A constant group has no variation, so its standardized values need an explicit convention.',
        'distance = value - mean\n# Divide this distance by a positive standard deviation.',
        ['Define `standard_scores(values)` for a list of finite numbers.',
         'Return a list of z-scores in input order, using the population standard deviation. Do not round.',
         'Return `[]` for empty input and all zeros for a constant list, including a one-item list. Leave the input unchanged.'],
        '''
        import math
        def standard_scores(values):
            if not values:
                return []
            mean=sum(values)/len(values)
            sd=math.sqrt(sum((x-mean)**2 for x in values)/len(values))
            return [(x-mean)/sd for x in values] if sd else [0.0]*len(values)
        ''',
        [('Use the population measure and preserve order', '''
          import numpy as np
          values=[8,2,5]; old=values.copy()
          assert np.allclose(standard_scores(values),[1.224744871391589,-1.224744871391589,0])
          assert values==old
          '''),
         ('Handle no variation and an empty sample', 'assert standard_scores([9,9])==[0,0] and standard_scores([2])==[0]\nassert standard_scores([])==[]')],
        ['Compute the mean before the squared deviations.', 'Population variance divides by the number of observations.', 'Handle zero standard deviation before division.'],
        'Standardization changes units, not the relative ordering of observations.')
    unit(m, 'bootstrap', 'Build a bootstrap interval',
        'Bootstrap resampling estimates how a statistic varies by sampling the observed values with replacement. Here the resampling index lists are supplied, making the calculation reproducible without depending on a random-number generator. A percentile interval summarizes the resampled means; it is not a guaranteed range for future individual observations.',
        'values = [4,9,12]\nindices = [2,2,0]\nresample = [values[i] for i in indices]',
        ['Define `bootstrap_interval(values, resamples)`. `values` is a nonempty list of finite numbers; `resamples` is a nonempty list of index lists.',
         'Every index list has the same length as `values` and contains valid zero-based indices; repeated indices are allowed. Compute the mean of each resample.',
         'Return `(lower, upper)` from the 2.5th and 97.5th percentiles of those means, using NumPy `quantile` with `method="linear"`. Do not round or modify inputs.'],
        '''
        import numpy as np
        def bootstrap_interval(values,resamples):
            means=[sum(values[i] for i in indices)/len(indices) for indices in resamples]
            lower,upper=np.quantile(means,[0.025,0.975],method="linear")
            return float(lower),float(upper)
        ''',
        [('Use repeated indices and percentile interpolation', '''
          import numpy as np
          assert np.allclose(bootstrap_interval([0,10],[[0,0],[0,1],[1,1]]),(0.25,9.75))
          '''),
         ('Handle constant and single-resample results', '''
          import numpy as np
          values=[2,6,10]; indices=[[0,1,2],[2,2,2]]
          assert np.allclose(bootstrap_interval(values,indices),(6.1,9.9))
          assert values==[2,6,10] and indices==[[0,1,2],[2,2,2]]
          assert bootstrap_interval([4],[[0]])==(4,4)
          ''')],
        ['Map each index list to a new sample of values.', 'Summarize each sample before taking quantiles.', 'Quantiles use probabilities 0.025 and 0.975, not percentages 2.5 and 97.5.'],
        'Reproducible resamples separate the interval calculation from the randomness used to generate samples.')
    unit(m, 'permutation', 'Compute an exact permutation p-value',
        'Under a no-effect null hypothesis for a randomized two-group experiment, group labels can be reassigned while holding group sizes fixed. An exact two-sided permutation test counts allocations whose absolute mean difference is at least the observed one. Repeated values remain distinct observations, so enumerate positions rather than unique values. This is feasible only for small datasets.',
        'from itertools import combinations\nallocations = list(combinations(range(4),2))\n# Each pair chooses positions for one group.',
        ['Define `permutation_pvalue(a, b)` for two nonempty lists of finite numbers, with at most 10 observations combined.',
         'Pool the observations. Enumerate every allocation of `len(a)` positions to group A; the other positions form group B.',
         'Return the fraction of allocations with an absolute difference in group means at least the observed absolute difference. Include equal differences, using a tolerance of `1e-12`. Do not round.'],
        '''
        from itertools import combinations
        def permutation_pvalue(a,b):
            values=list(a)+list(b)
            observed=abs(sum(a)/len(a)-sum(b)/len(b))
            extreme=total=0
            for picked in combinations(range(len(values)),len(a)):
                chosen=set(picked)
                left=[x for i,x in enumerate(values) if i in chosen]
                right=[x for i,x in enumerate(values) if i not in chosen]
                difference=abs(sum(left)/len(left)-sum(right)/len(right))
                extreme += difference >= observed-1e-12
                total += 1
            return extreme/total
        ''',
        [('Count both tails and all allocations', 'assert abs(permutation_pvalue([1,2],[5,6])-1/3)<1e-12\nassert abs(permutation_pvalue([0],[1,2])-2/3)<1e-12'),
         ('Count tied observations as distinct positions', 'assert permutation_pvalue([3,3],[3,3])==1\nassert abs(permutation_pvalue([0,0],[1,1])-1/3)<1e-12')],
        ['Enumerate combinations of positions, not combinations of distinct values.', 'Keep both group sizes fixed for each allocation.', 'Use an absolute statistic to include differences in either direction.'],
        'A p-value measures how unusual the observed statistic is under the specified null allocation model. It is not the probability that the null hypothesis is true.')
    unit(m, 'lift', 'Separate percentage points from relative lift',
        'A conversion rate can be compared in two ways. Percentage-point change is 100 times the difference between rates. Relative lift divides that difference by the baseline rate and expresses it as a percentage. A zero baseline makes relative lift undefined, even when the absolute change is clear.',
        'old_rate = 0.20\nnew_rate = 0.25\n# The absolute change and the relative change use different denominators.',
        ['Define `conversion_lift(control_success, control_total, variant_success, variant_total)`.',
         'Inputs are integer counts with positive totals and successes between zero and their total. Return a dictionary with `control_rate`, `variant_rate`, `point_change`, `relative_lift`.',
         'Rates are fractions from 0 to 1. `point_change` is variant minus control in percentage points. `relative_lift` is that rate change divided by the control rate, multiplied by 100. Use `None` for relative lift when the control rate is zero. Do not round.'],
        '''
        def conversion_lift(control_success,control_total,variant_success,variant_total):
            control=control_success/control_total
            variant=variant_success/variant_total
            return {"control_rate":control,"variant_rate":variant,
                    "point_change":100*(variant-control),
                    "relative_lift":100*(variant-control)/control if control else None}
        ''',
        [('Use the correct units', '''
          r=conversion_lift(20,100,30,100)
          assert set(r)=={"control_rate","variant_rate","point_change","relative_lift"}
          assert abs(r["point_change"]-10)<1e-12 and abs(r["relative_lift"]-50)<1e-12
          assert r["control_rate"]==0.2 and r["variant_rate"]==0.3
          '''),
         ('Handle unequal sizes and a zero baseline', 'r=conversion_lift(4,8,2,8)\nassert r["point_change"]==-25 and r["relative_lift"]==-50\nr=conversion_lift(0,10,1,5)\nassert r["relative_lift"] is None and r["point_change"]==20')],
        ['Calculate each rate from its own group size.', 'Keep fractional rates separate from percentage units.', 'A negative lift indicates a decrease from the control rate.'],
        'Clear units keep a report from confusing a small absolute change with a large relative one.')
    unit(m, 'experiment-project', 'Project · report a small experiment',
        'A fictional randomized pilot compares completion times for two layouts. Lower time is better. Calculate both an effect size and an exact two-sided permutation p-value; report evidence conservatively using a prespecified 0.05 threshold. These tiny samples are for learning the workflow, not a reliable business recommendation.',
        'difference = variant_mean - control_mean\n# A negative difference means the variant was faster.',
        ['Read `pilot.csv`, which has `group` (`control` or `variant`) and numeric `seconds`. All rows are valid.',
         'Write `experiment.json` with exactly `control_mean`, `variant_mean`, `difference`, `p_value`, `decision`. `difference` is variant mean minus control mean.',
         'Calculate an exact two-sided permutation p-value for the absolute mean difference by enumerating all fixed-size group allocations, including ties with tolerance `1e-12`. Keep numeric results unrounded.',
         'Set `decision` to `"evidence of a difference"` when `p_value < 0.05`, otherwise `"insufficient evidence"`. Also write `conclusion.txt` with two nonempty lines: describe which observed mean is lower, then explain why the result does not prove the layouts are equivalent. The wording is yours; review its meaning yourself.'],
        '''
        import csv,json
        from itertools import combinations
        with open("pilot.csv",newline="") as f:
            rows=list(csv.DictReader(f))
        a=[float(r["seconds"]) for r in rows if r["group"]=="control"]
        b=[float(r["seconds"]) for r in rows if r["group"]=="variant"]
        control=sum(a)/len(a); variant=sum(b)/len(b)
        values=a+b; observed=abs(variant-control)
        extreme=total=0
        for picked in combinations(range(len(values)),len(a)):
            chosen=set(picked)
            left=[v for i,v in enumerate(values) if i in chosen]
            right=[v for i,v in enumerate(values) if i not in chosen]
            extreme += abs(sum(left)/len(left)-sum(right)/len(right)) >= observed-1e-12
            total += 1
        p=extreme/total
        report={"control_mean":control,"variant_mean":variant,"difference":variant-control,
                "p_value":p,"decision":"evidence of a difference" if p<0.05 else "insufficient evidence"}
        with open("experiment.json","w") as f: json.dump(report,f)
        with open("conclusion.txt","w") as f:
            f.write("The variant had a lower observed mean completion time.\\nThe pilot is too small to establish equivalence; insufficient evidence is not proof of no difference.\\n")
        ''',
        [('Report effect size and exact evidence', '''
          import json
          with open("experiment.json") as f: r=json.load(f)
          assert set(r)=={"control_mean","variant_mean","difference","p_value","decision"}
          assert r["control_mean"]==14 and r["variant_mean"]==9 and r["difference"]==-5
          assert abs(r["p_value"]-0.1)<1e-12 and r["decision"]=="insufficient evidence"
          '''),
         ('Include a written interpretation for self-review', '''
          from pathlib import Path
          lines=[line.strip() for line in Path("conclusion.txt").read_text().splitlines() if line.strip()]
          assert len(lines)==2
          ''')],
        ['Reuse the allocation logic from the permutation exercise.', 'Compute the signed effect separately from the absolute test statistic.', 'Insufficient evidence for a difference does not establish equivalence.'],
        'Effect size, uncertainty and study design belong together. The automated check verifies the numeric report and the presence of two interpretation lines; it does not grade the meaning of your prose.',
        files={'pilot.csv':'group,seconds\ncontrol,12\ncontrol,14\ncontrol,16\nvariant,7\nvariant,9\nvariant,11\n'},
        exports=['experiment.json','conclusion.txt'],kind='project',minutes=45)

    from course_sql_models import extend_sql_models
    extend_sql_models(section, unit)
