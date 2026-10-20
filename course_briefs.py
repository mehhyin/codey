"""Learner-facing task contracts. Describe the destination, not the solution."""

BRIEFS = {
    'basics-variables': [
        'A notebook costs 12.50 and you are buying 4. Create the input variables `price` and `quantity` shown above.',
        'Create a numeric variable named `total` containing the cost of all the notebooks. Calculate it from the inputs.',
        'Print `total` once. The console should show the cost, without a label or other text.',
    ],
    'basics-types': [
        'Create a variable named `joined` containing `left_text` followed by `right_text`. Use the two text inputs; keep the result as text.',
        'Create a variable named `added` containing the arithmetic sum of `left_number` and `right_number`.',
        'Create `text_type` containing the type name of `joined`, as text. Create `number_type` containing the type name of `added`, also as text.',
    ],
    'basics-precedence': [
        'Compare two ways of charging a handling fee for the same order. Use `price`, `fee` and `quantity` from the starting data.',
        'Create `per_item_total`: the complete order cost when the handling fee is charged separately for every item.',
        'Create `per_order_total`: the complete order cost when the handling fee is charged just once for the whole order.',
    ],
    'basics-division': [
        'You have `photos` photos and each page holds `per_page` photos. Use the three division operators from the lesson.',
        'Create `full_pages`: the number of pages you can fill completely, using `//`.',
        'Create `leftover_photos`: the number of photos remaining after those full pages, using `%`.',
        'Create `average_pages`: the ordinary division result, including its fractional part, using `/`. Do not round it up to a whole page.',
    ],
    'basics-updates': [
        'Create `balance` from the starting data, then create `opening` to remember that starting balance.',
        'Update `balance` after a purchase costing 25, then update it again after a refund of 7.',
        'Create `closing` containing the final balance. Leave `opening` holding the original amount.',
    ],
    'basics-strings': [
        'Use the input variables `item` and `total` to create a string variable named `message`.',
        'Its text must be exactly `Notebook: 50.00`: the item name, a colon and space, then the amount with two decimal places.',
        'Print `message` once, with no extra text. The surrounding quotation marks are not part of the message.',
    ],
    'basics-text-methods': [
        'Create a string variable named `cleaned` from `raw`: remove whitespace at the two ends, make the letters lowercase, and replace each remaining space with an underscore.',
        'Keep the original value of `raw` unchanged.',
    ],
    'basics-split-join': [
        'Create a list named `parts` containing the separate steps in `raw`. The `|` character separates one step from the next and should not appear in the list items.',
        'Create a string named `display` containing those steps in the same order, separated by ` → `, including one space on each side of the arrow.',
        'Create `first` containing the first item from `parts`.',
    ],
    'basics-conversion': [
        'The starting price and quantity are text. Create `price` as a floating-point number converted from `price_text`.',
        'Create `quantity` as an integer converted from `quantity_text`.',
        'Create `total` containing the cost of buying that quantity at that price. Calculate it using the converted numbers.',
    ],
    'basics-debug-types': [
        'Copy the code in “Code to fix” into your editor and correct its calculation. Keep the original input values.',
        'The variable `total` must contain the numeric cost of `quantity` items at the price in `price_text`, rather than repeated text.',
        'Print the numeric `total` once, with no label or extra output.',
    ],
    'basics-receipt-review': [
        'Work out each person’s share of a restaurant bill. `food_text` is the food cost stored as text; `service` is an additional charge for the whole group.',
        'Create a numeric variable named `each` containing the complete bill divided equally among `people`.',
        'Create a string variable named `message` containing `Each person pays ` followed by `each` formatted to two decimal places.',
    ],
    'basics-trip-1': [
        'Create three numeric input variables: `nights` is 3, `nightly_rate` is 80, and `transport` is 45 for the whole trip.',
        'Create `accommodation` containing the cost of the stay for all nights.',
        'Create `essentials` containing the combined accommodation and transport cost.',
    ],
    'basics-trip-2': [
        'Use the starting `budget` and `essentials`. Also create `food_per_day` with value 25 and `days` with value 4.',
        'Create `food_total` containing the food allowance for the entire trip.',
        'Create `trip_total` containing the essentials and food costs together.',
        'Create `remaining` containing the money left from the budget after paying the full trip cost.',
    ],
    'basics-trip-3': [
        'Use the starting variables `trip_total` and `remaining` to create a string variable named `summary`.',
        'Format it exactly as `Trip: 385.00 | Left: 65.00`, with two decimal places for each amount and the spaces shown.',
        'Print `summary` once, without quotation marks or additional text.',
    ],
    'flow-conditions': [
        'Compare the amount `spent` with the available `budget`.',
        'Create a string variable named `status`. Store `"over"` when spending is greater than the budget; store `"within"` otherwise, including when they are equal.',
        'Keep the starting values of `spent` and `budget` unchanged.',
    ],
    'flow-boundary': [
        'Create three Boolean variables by comparing `score` with 70.',
        '`above` should say whether the score is strictly greater than 70. `qualifies` should say whether it is at least 70.',
        '`different` should say whether the score is not equal to 70. Use comparisons so the values are `True` or `False`, not strings.',
    ],
    'flow-boolean': [
        'Create a Boolean variable named `discount_allowed`: true only when the customer is a `member` and their `spend` is at least 50.',
        'Create `can_fulfil`: true when either pickup is selected (`pickup`) or a delivery address is available (`has_address`).',
        'Create `needs_address`: true only when pickup is not selected and no address is available. Each result must be a Boolean.',
    ],
    'flow-for': [
        'Use a `for` loop to calculate the sum of every amount in `expenses`. Store the result in the numeric variable `total`.',
        'Print the final `total` once, after the loop. Do not print a separate running total for each expense.',
    ],
    'flow-range': [
        'Use `range()` to create a list named `evens` containing every even integer from 2 through 10, including both ends, in ascending order.',
        'Create a numeric variable named `total` containing the sum of the numbers in `evens`.',
    ],
    'flow-while': [
        'Start with `savings` of 20 and `weeks` of 0. Each week adds 15 to the savings.',
        'Use a `while` loop to add one week at a time, stopping as soon as the savings reaches or exceeds 80.',
        'After the loop, `savings` must contain the final amount and `weeks` must contain the number of weekly additions.',
    ],
    'flow-filter': [
        'Create a list named `large` containing only the amounts in `expenses` that are at least 20. Include amounts equal to 20.',
        'Keep the same order as the input, including repeated amounts that qualify.',
    ],
    'flow-break': [
        'Search `temperatures` from left to right. Store the first reading strictly above 30 in the variable `first_hot`.',
        'Use `break` to stop the loop at that first match. Later hot readings must not replace it.',
    ],
    'flow-enumerate': [
        'Each item in `spending` represents one day. The first item is day 1, the second is day 2, and so on.',
        'Create a list named `alert_days` containing the day numbers where spending was strictly greater than 30. Store day numbers, not spending amounts, in chronological order.',
    ],
    'flow-debug-total': [
        'Copy the code in “Code to fix” into your editor. Correct it so `total` contains the sum of all numbers in `values`.',
        'Print the final `total` exactly once, after the loop has finished.',
    ],
    'flow-stock-review': [
        'Create a list named `labels` with one stock-status string for each number in `quantities`, in the same order.',
        'Use `"out"` for zero, `"low"` for 1 through 4, and `"healthy"` for 5 or more.',
        'Create an integer named `urgent_count` containing the number of quantities below 5, including zeros.',
    ],
    'flow-alert-1': [
        'The list `daily` contains one spending amount for each day of the week. Create `total` containing the sum for the entire week.',
        'Create a list named `high_days` containing the spending amounts strictly greater than 30, in their original order. This list contains amounts, not day numbers.',
        'Create `high_count` containing the number of entries in `high_days`.',
    ],
    'flow-alert-2': [
        'Create a string variable named `status` by comparing `total` with `budget`: use `"over budget"` if greater, `"at budget"` if equal, and `"under budget"` if smaller.',
        'Create a string variable named `report` using `total`, `status` and `high_count`. Its format is `200 spent | at budget | 3 high days` for these inputs.',
    ],
    'collections-lists': [
        'Using the list `readings`, create `first` containing its first value and `last` containing its final value.',
        'Create a separate list named `ordered` containing all readings sorted from smallest to largest. Leave `readings` in its original order.',
    ],
    'collections-slices': [
        'Create three new lists from `observations`: `first_three` contains its first three values, and `last_two` contains its final two values.',
        '`middle` must contain the values at zero-based indices 1, 2 and 3, in that order. Use list slicing.',
    ],
    'collections-mutations': [
        'Update the existing list `steps`: append `"clean"`, then extend the list with `"analyse"` and `"export"` as two separate items.',
        'Remove the last item using `pop()` and save that removed string in `postponed`. Keep the remaining items in `steps`.',
    ],
    'collections-copies': [
        'Create a separate list named `revised` with the same initial values as `original`.',
        'Change the first value in `revised` to 99, then add 40 to its end.',
        'The values in `original` must remain unchanged when you edit `revised`.',
    ],
    'collections-dicts': [
        'Use the dictionary `order` to create `subtotal`, the cost of the given quantity before any discount.',
        'Create `discount` containing the order’s discount amount. If the dictionary has no `"discount"` key, use zero. This is a money amount, not a percentage.',
        'Add a `"total"` key to `order` containing the subtotal after deducting the discount.',
    ],
    'collections-sets': [
        'Create a set named `missing` containing filenames that appear in `expected` but not in `received`.',
        'Create a set named `unexpected` containing filenames that appear in `received` but not in `expected`.',
        'Create a set named `shared` containing filenames present in both input sets. Store these results in variables; no function is required.',
    ],
    'collections-items': [
        'The dictionaries `stock` and `prices` use the same product names as keys. Create a dictionary named `values` mapping each product to the value of all its units in stock.',
        'Create a numeric variable named `inventory_value` containing the combined value of every product.',
    ],
    'collections-comprehensions': [
        'Create a list named `cleaned` from `names`. For each name, remove whitespace at the two ends and make the letters lowercase.',
        'Exclude names that are empty after whitespace is removed. Keep the remaining names in their original order, including duplicates.',
    ],
    'collections-frequency': [
        'Clean each string in `channels` by removing whitespace at its ends and making it lowercase. Ignore strings that become empty.',
        'Create a dictionary named `counts`: each key is a cleaned channel name, and its value is the number of times that name occurs.',
    ],
    'collections-nested': [
        'Read the nested dictionary `order`. Create `city` containing the customer’s city.',
        'Create `units` containing the sum of the `"qty"` values across all records in `order["items"]`.',
        'Create `first_product` containing the `"name"` of the first item in that list.',
    ],
    'collections-restock-review': [
        'Create a list named `restock` containing only products whose current stock is below `target`.',
        'Represent each included product with a dictionary containing exactly `"name"` (its name) and `"buy"` (the number of extra units needed to reach the target).',
        'Sort `restock` alphabetically by product name. Do not change the input list `products` or its records.',
    ],
    'collections-shop-1': [
        'Each record in `orders` describes a sale: `"price"` is the price of one unit and `"qty"` is the number sold.',
        'Create a list named `line_totals` containing the revenue of each order, in input order.',
        'Create `revenue` containing the combined revenue, and `units` containing the total number of units sold across all orders.',
    ],
    'collections-shop-2': [
        'Create a dictionary named `by_item` mapping each product name in `orders` to its total revenue across every order for that product.',
        'Create a string variable named `top_item` containing the product name with the highest total revenue. Compare revenue, not the number of units sold.',
    ],
    'functions-return': [
        'Define a function named `line_total` with two parameters, `price` and `quantity`.',
        'Return the numeric cost of buying that quantity at the given unit price. Support decimal prices and a quantity of zero.',
        'Return the value to the caller; printing it alone does not satisfy this task.',
    ],
    'functions-print-return': [
        'Copy the function in “Code to fix” and repair `tax(amount)` so a caller receives a numeric result.',
        'Return 6% of the supplied `amount`. The function must work for different nonnegative amounts, including zero; printing the value is not enough.',
    ],
    'functions-scope': [
        'Define `add_values(values)` to return the sum of the numbers in its input list, using an accumulator local to the function.',
        'Each call must start a new calculation: earlier calls must not affect later results. Return zero for an empty list.',
    ],
    'functions-defaults': [
        'Define `discounted(amount, percent=10)`. Here `percent` is the percentage taken off the original amount.',
        'Return the amount left to pay after the discount, rounded to two decimal places. Use a 10% discount when the caller omits `percent`.',
        'A zero-percent discount must leave the amount unchanged.',
    ],
    'functions-keywords': [
        'Re-create the `shipping` function shown in the helper reference before calling it.',
        'Create `express_total` from a call with a basket of 40, a fee of 12 and a discount of 5.',
        'Create `standard_total` from a call with a basket of 40 and a discount of 5, leaving the fee at its default. Pass optional values by keyword.',
    ],
    'functions-tuples': [
        'Define `split_minutes(total)` for a nonnegative whole number of minutes.',
        'Return a two-item tuple: the number of complete hours first, then the minutes left over. For example, 75 minutes would return `(1, 15)`.',
        'Use floor division and remainder. Handle zero and durations shorter than one hour.',
    ],
    'functions-validation': [
        'Define `parse_quantity(text)`. The caller will supply a string.',
        'Return its integer value when it contains valid nonnegative integer text, including zero.',
        'Return `None` for negative integers, decimal text or text that cannot be converted to an integer. These inputs should not crash the function.',
    ],
    'functions-guards': [
        'Define `average_price(prices)` to return the arithmetic mean of the numbers in the list, rounded to two decimal places.',
        'Count zero prices as valid entries. Return `None` if the list is empty.',
    ],
    'functions-compose': [
        'Re-create the supplied `subtotal` and `add_tax` helper functions, then define `invoice_total(prices)`.',
        'Use the two helpers to calculate the basket total including 6% tax. Return one numeric result rounded to two decimal places, rounding only at the end.',
        'An empty basket should return zero.',
    ],
    'functions-raise': [
        'Define `as_percent(fraction)` to return the numeric percentage represented by a fraction between 0 and 1, inclusive. For example, 0.5 represents 50%.',
        'For a fraction below 0 or above 1, raise `ValueError` with a nonempty explanatory message instead of returning a percentage.',
    ],
    'functions-clean-review': [
        'Define `unique_names(names)` to return a new list of names with surrounding whitespace removed and letters lowercased.',
        'Exclude blank names and keep only the first occurrence of each cleaned name. Preserve the order of those first occurrences.',
        'Do not modify the input list. An empty list must return an empty list.',
    ],
    'functions-receipt-1': [
        'Define `subtotal(items)`. Each item is a dictionary with `"price"` (unit price) and `"qty"` (quantity).',
        'Return the combined cost of every item. Return zero for an empty list.',
        'Leave the input list and its dictionaries unchanged.',
    ],
    'functions-receipt-2': [
        'Define `checkout(amount, discount=0, tax=6)`. Both `discount` and `tax` are percentages. Apply the discount first, then charge tax on the discounted amount.',
        'Return a dictionary with exactly four keys: `"subtotal"` is the original amount, `"discount_amount"` is the money deducted, `"tax_amount"` is the money added as tax, and `"total"` is the final amount due.',
        'Calculate with unrounded intermediate values, then round each value placed in the returned dictionary to two decimal places. Support a zero amount.',
    ],
    'files-text': [
        'Read the provided file `tasks.txt` and create a list named `tasks`, with one cleaned task string per nonblank line.',
        'Remove whitespace at the start and end of each line. Ignore lines that become empty, and preserve the remaining lines’ order.',
        'Create an integer named `count` containing the number of tasks in that list.',
    ],
    'files-line-counts': [
        'Read the provided `log.txt` file line by line and create two integer variables.',
        '`raw_count` must count every line, including blank lines. `useful_count` must count only lines that contain something other than whitespace.',
    ],
    'files-append': [
        'Update the provided file `events.txt` by adding a new final line containing `exported`.',
        'Preserve the existing two lines in order, and end the new line with a newline character. The result must be saved in the file.',
    ],
    'files-csv': [
        'Read the provided `sales.csv` with `csv.DictReader` and store the data records as a list named `rows`. Do not include the header as a data row.',
        'Create `revenue` containing the combined sale value: each row has a unit `price` and a `quantity`. Convert CSV text to numbers where needed.',
        'Create `row_count` containing the number of data records.',
    ],
    'files-quoted': [
        'Read `products.csv` using `csv.DictReader` and store the data records in a list named `rows`.',
        'Create `first_name` containing the full name of the first product, including any comma inside that name.',
        'Create `units` containing the sum of all `qty` values as a number.',
    ],
    'files-write-csv': [
        'Create a file named `stock.csv` from the input list `records`.',
        'The CSV must have a header with columns `name` then `qty`, followed by every record in input order.',
        'Use CSV writing tools so a comma inside a product name stays part of that field.',
    ],
    'files-json': [
        'Read the provided `settings.json` into a dictionary variable named `settings`.',
        'Increase its `"target"` value by 5, keeping its `"name"` value unchanged.',
        'Save the updated dictionary as valid JSON in a new file named `updated.json`.',
    ],
    'files-nested-json': [
        'Read `response.json` into a variable named `payload`. The records to analyse are inside its `"data"` list.',
        'Create a list named `names` containing each record’s `"name"`, in input order.',
        'Create `total_units` containing the sum of the records’ numeric `"units"` values.',
    ],
    'files-defaults': [
        'Read the order records in `orders.json` and create a list named `totals`, with one amount per order in input order.',
        'An order’s amount is the cost of its quantity at its unit price, less its discount. Treat a missing `"discount"` as zero.',
        'Discounts here are money amounts, not percentages.',
    ],
    'files-rejected': [
        'Read every line of `amounts.txt`, remove surrounding whitespace, and try to interpret it as an integer.',
        'Create a list named `valid` containing the successfully parsed integers in order. Include zero and negative integers.',
        'Create an integer named `rejected` counting lines that could not be parsed, including blank lines and decimal text.',
    ],
    'files-merge-review': [
        'Read `jan.csv` followed by `feb.csv`. Create a list named `combined` containing their data-row dictionaries in that order, keeping CSV field values as strings.',
        'Create a numeric variable named `revenue` containing the sum of the `"amount"` field across all records.',
        'Write the combined records to `combined.csv`, with one header in the order `month,amount` and no repeated headers between months.',
    ],
    'files-contacts-1': [
        'Read the provided `contacts.csv` and create a list named `cleaned`.',
        'Each retained record must be a dictionary with `"name"` stripped of surrounding whitespace and `"email"` stripped and lowercased.',
        'Exclude records whose email becomes blank. Keep duplicates and preserve input order in this step.',
    ],
    'files-contacts-2': [
        'Create a list named `unique` from `cleaned`, keeping only the first record for each distinct email address. Preserve the order of those first records.',
        'Write `unique` to `clean_contacts.csv` with columns `name` then `email`, including the header.',
        'Open the output file with `newline=""` when writing CSV.',
    ],
    'analysis-statistics': [
        'Use the delivery times in `minutes` to create three numeric variables.',
        '`average` must contain the arithmetic mean, `middle` the median, and `spread` the difference between the longest and shortest delivery times.',
        'Keep the results numeric and do not round them.',
    ],
    'analysis-proportions': [
        'Create `delivery_rate`: the percentage of placed orders that were delivered. Use `placed` as the comparison total.',
        'Create `punctuality_rate`: the percentage of delivered orders that arrived on time. Use `delivered` as the comparison total.',
        'Store each percentage as a number rounded to one decimal place, where 100 means 100%. Do not add a percent sign or convert it to text.',
    ],
    'analysis-weighted': [
        'Define `weighted_mean(means, counts)`. The lists have matching positions: each mean belongs to a group with the corresponding number of observations.',
        'Return the overall mean with larger groups contributing proportionally more. The lists have equal lengths and the counts are nonnegative.',
        'Do not round. Return `None` when the total count is zero, including when both lists are empty.',
    ],
    'analysis-outliers': [
        'Create a numeric variable named `threshold` containing twice the median of `values`.',
        'Create a list named `flagged` containing only input values strictly greater than that threshold, in input order.',
        'Keep `values` unchanged.',
    ],
    'analysis-spread': [
        'For the lists `a` and `b`, create `mean_a` and `mean_b` containing their arithmetic means.',
        'Create `spread_a` and `spread_b` containing their population standard deviations, without rounding. Use the population measure, not the sample measure.',
        'Create a string variable named `more_variable`: use `"B"` if group B has the greater standard deviation, otherwise `"A"`.',
    ],
    'analysis-missing': [
        'Define `safe_mean(values)` to return the arithmetic mean after excluding entries that are `None`.',
        'Zero is a valid observation and must count toward the mean. Return `None` if no valid entries remain, including for an empty list.',
    ],
    'analysis-group-means': [
        'The records in `rows` have a `"team"` and a delivery time in `"minutes"`. Summarise each team separately.',
        'Create a dictionary named `counts` mapping each team to its number of records.',
        'Create a dictionary named `average_by_team` mapping each team to its mean delivery time. Use that team’s own records and count.',
    ],
    'analysis-growth': [
        'Define `growth(previous, current)` to return the percentage change from the previous value to the current value, using the previous value as the baseline.',
        'Round to one decimal place. An increase should be positive, a decrease negative, and no change zero.',
        'Return `None` when `previous` is zero because the percentage change has no valid baseline.',
    ],
    'analysis-rolling': [
        'Define `moving_average(values)` to return a list of averages for consecutive groups of three observations.',
        'The first result uses the first three values, the next uses values 2 through 4, and so on. Keep these results in chronological order and do not round.',
        'Include only full groups of three. Return an empty list if fewer than three values are supplied.',
    ],
    'analysis-rank-ties': [
        'Define `rank_names(rows)`, where each record has a `"name"` and a numeric `"score"`.',
        'Return a list of names ordered from highest score to lowest. If scores are equal, put those names in alphabetical order.',
        'Return names only, not the complete records. Handle negative scores and return an empty list for empty input.',
    ],
    'analysis-audit-review': [
        'Define `summarise(values)` to return a dictionary with exactly `"valid_count"`, `"missing_count"`, `"mean"` and `"maximum"`.',
        'Treat only `None` as missing. Count all other values, including zero, as valid observations.',
        'Calculate the mean and maximum from valid values only, rounding the mean to two decimal places.',
        'If no valid observations exist, return `None` for both the mean and maximum. An empty input has both counts equal to zero.',
    ],
    'analysis-report-1': [
        'Read the order records in `orders.csv`. Create a dictionary named `region_totals` mapping each region to the sum of its revenue values.',
        'Create `total_revenue` containing revenue across all regions.',
        'Create a string named `top_region` containing the name of the region with the largest revenue total.',
    ],
    'analysis-report-2': [
        'Use `region_totals` to create a dictionary named `shares`, mapping each region to its percentage of the combined revenue. Round percentages to one decimal place.',
        'Create a list named `ranking` containing region names from highest total revenue to lowest.',
        'Create a string named `summary` naming the leading region and its share. For these inputs its exact format is `North leads with 44.0% of revenue.`',
    ],
    'pandas-table': [
        'Use pandas to read the provided `sales.csv` into a DataFrame variable named `df`.',
        'Add a column named `"revenue"` to `df`, containing the sale value of each row from its quantity and unit price.',
        'Create a numeric variable named `total_revenue` containing the sum of that column.',
    ],
    'pandas-inspect': [
        'Create the starting DataFrame `df` using pandas. Create `row_count` and `column_count` from its shape.',
        'Create a Python list named `columns` containing the column names in their original order.',
        'Create a DataFrame named `preview` containing only the first two rows. Keep every original row in `df`.',
    ],
    'pandas-loc-iloc': [
        'Create `by_label` containing the scalar `"sales"` value in the row whose index label is 20.',
        'Create `by_position` containing the scalar `"sales"` value in the first row, regardless of that row’s index label.',
        'Create a DataFrame named `chosen` with all input rows but only the columns `"city"` and `"sales"`, in that order.',
    ],
    'pandas-select': [
        'From `df`, keep records whose region is exactly `"North"` and whose revenue is at least 100, including 100.',
        'Order those records from highest revenue to lowest, then create a Python list named `products` containing their product names in that order.',
    ],
    'pandas-rename': [
        'Create a DataFrame named `clean` from `raw`, renaming `"Product Name"` to `"product"` and `"Units Sold"` to `"units"`.',
        'Keep the column names and data in `raw` unchanged.',
        'Create a numeric variable named `total_units` containing the sum of the `"units"` column in `clean`.',
    ],
    'pandas-clean': [
        'Clean the DataFrame `df` and keep the finished result in the same variable name.',
        'Remove surrounding whitespace from every `"category"` value and make it lowercase.',
        'Convert `"amount"` values to numbers. Discard rows with amounts that cannot be converted; retain valid zero amounts.',
        'Reset the remaining row index to consecutive integers starting at zero, without adding an index column.',
    ],
    'pandas-deduplicate': [
        'Normalise the `"email"` column in `df` by removing surrounding whitespace and making it lowercase.',
        'Create a DataFrame named `latest` containing only the last record for each cleaned email. Preserve the relative order of the retained rows.',
        'Keep the columns `"email"` and `"visits"`. Reset the row index to consecutive integers starting at zero without adding an extra column.',
    ],
    'pandas-fill-policy': [
        'In `df`, replace missing values in the `"discount"` column with zero. Leave missing `"revenue"` values missing.',
        'Add a column named `"net"` containing revenue after its discount. A row with unknown revenue must also have unknown net revenue.',
        'Create an integer named `missing_revenue` containing the number of rows with missing revenue.',
    ],
    'pandas-aggregations': [
        'Create a DataFrame named `summary` with one row per region in `df`.',
        'Use these columns, in order: `"region"` (region name), `"total"` (sum of revenue), `"average"` (mean revenue), and `"order_count"` (number of orders).',
        'Sort by region name alphabetically and use a consecutive row index starting at zero. Region must be a column, not the index.',
    ],
    'pandas-merge': [
        'Create a DataFrame named `joined` by matching `orders` with `products` on `"product_id"`. Keep every order in its original order, even if no product matches.',
        'Add a `"revenue"` column to `joined`, calculated from each row’s quantity and matched price. Unmatched revenue must remain missing.',
        'Create an integer named `unmatched` counting rows with no matching price.',
    ],
    'pandas-monthly-review': [
        'Interpret the `"date"` column in `df` as dates. Create an integer named `rejected` counting invalid dates, then leave those records out of the summary.',
        'Create a DataFrame named `monthly` with one row per month and columns `"month"` and `"total"`. The total is the sum of valid records’ revenue for that month.',
        'Write month labels as strings in `YYYY-MM` format and order rows from earliest month to latest.',
    ],
    'pandas-explore-1': [
        'Read `shop.csv` into a pandas DataFrame named `df` and clean its `"product"` values by stripping surrounding whitespace and lowercasing.',
        'Convert `"quantity"` to numeric values. Remove rows whose quantity is invalid, but keep rows with zero quantity.',
        'Add a `"revenue"` column containing each row’s sale value from quantity and price.',
        'Keep the cleaned result in `df` with a consecutive index starting at zero and no additional index column.',
    ],
    'pandas-explore-2': [
        'Create a DataFrame named `summary` with one row per product and columns `"product"` and `"revenue"`. Revenue must be the combined revenue for that product in `df`.',
        'Sort the summary from highest revenue to lowest and reset its row index.',
        'Save it to `product_summary.csv` with the two named columns and no index column.',
        'Create a string variable named `top_product` containing the leading product’s name.',
    ],
    'automation-paths': [
        'Inspect the provided `inbox` directory. Create a list named `text_files` containing the names of its direct files with a `.txt` extension, ignoring extension letter case.',
        'Store filenames only, without the `inbox/` prefix, and sort them alphabetically using Python’s normal string ordering. Do not search inside subdirectories.',
    ],
    'automation-recursive': [
        'Create a list named `direct` containing paths to `.csv` files directly inside `inbox`.',
        'Create a list named `recursive` containing paths to `.csv` files anywhere under `inbox`, including nested directories.',
        'Each list must be sorted and contain string paths beginning with `inbox/`, using forward slashes.',
    ],
    'automation-hashes': [
        'Define `same_content(first, second)`, where both arguments are paths to existing files.',
        'Compare the files’ bytes using SHA-256 hashes. Return the Boolean `True` when their contents match and `False` otherwise, even if the filenames differ.',
    ],
    'automation-dates': [
        'Define `report_name(date_text)` for an input date string in `YYYY-MM-DD` format.',
        'Return a filename string in `sales_YYYYMMDD.csv` format. Do not create a file.',
        'Validate the calendar date: impossible dates must raise `ValueError`, while valid leap days must work.',
    ],
    'automation-date-window': [
        'Define `week_window(end_text)`, where the argument is a date string in `YYYY-MM-DD` format.',
        'Return a tuple `(start, end)` containing two date strings in the same format. The window must include exactly seven calendar days, counting the supplied end date as the final day.',
        'Use `date.fromisoformat` and `timedelta`; the window must work across month and leap-year boundaries.',
    ],
    'automation-regex-extract': [
        'Search the input string `text` for invoice identifiers with the prefix `INV-` followed by exactly three digits.',
        'Create a list named `invoice_ids` containing just those three-digit portions as strings, in their order of appearance. Preserve leading zeros.',
        'Do not accept shorter identifiers or the first three digits of a longer identifier.',
    ],
    'automation-regex-clean': [
        'Define `clean_label(text)` to return one cleaned string.',
        'Replace each run of whitespace, including spaces, tabs and newlines, with one ordinary space. Remove whitespace at the two ends and make all letters lowercase.',
        'An input containing only whitespace must return an empty string.',
    ],
    'automation-copy': [
        'Define `copy_if_new(source, destination)` for two file paths. The source file and destination’s parent directory already exist.',
        'If the destination already exists, leave its contents untouched and return `False`.',
        'Otherwise create a copy there and return `True`. Keep the source file in both cases, including on repeated calls.',
    ],
    'automation-log-summary': [
        'Define `count_events(events)`. Each event is a dictionary whose `"status"` should be `"copied"`, `"skipped"` or `"failed"`.',
        'Return a dictionary containing all three status names as keys and their occurrence counts as integer values. Include zero counts, even for an empty input.',
        'Raise `ValueError` if any event has an unrecognised status.',
    ],
    'automation-collisions': [
        'Define `collisions(plan)`. Each plan record contains a destination path under its `"destination"` key.',
        'Return a sorted list of destination strings that occur in more than one record. Include each conflicting destination only once.',
        'Return an empty list if the plan is empty or every destination is unique.',
    ],
    'automation-manifest-review': [
        'Inspect only direct files inside `inbox` and create a list named `manifest`, sorted by filename. Ignore subdirectories and their contents.',
        'Each record must have `"name"` (filename without its parent path), `"bytes"` (file size in bytes), and `"sha256"` (the hexadecimal SHA-256 digest of its contents).',
        'Save that list as valid JSON in `manifest.json`.',
    ],
    'automation-organise-1': [
        'Create a list named `plan` describing where the direct files in `inbox` should be copied. Do not copy or move files in this step.',
        'Route `.txt` files to the `documents` category, `.csv` files to `data`, and other extensions to `other`. Compare extensions without regard to letter case.',
        'Each record must contain `"source"` as `inbox/<filename>` and `"destination"` as `organised/<category>/<filename>`, with forward slashes and the original filename preserved.',
        'Sort the plan by source filename using normal string ordering. Exclude directories and nested files.',
    ],
    'automation-organise-2': [
        'Define `apply_plan(plan)`, where each record provides `"source"` and `"destination"` file paths.',
        'For a destination that does not exist, create any needed parent directories and copy the source file there. Preserve every source file.',
        'Skip destinations that already exist without changing their contents.',
        'Return a dictionary with `"copied"` and `"skipped"` counts. Include both keys with zero values for an empty plan.',
    ],
    'web-html': [
        'Define `heading(name)` to return an HTML string with the supplied name inside a single `<h1>` element.',
        'Escape special HTML characters in the name so input text is displayed as text, not interpreted as markup.',
        'Return only the heading fragment, without spaces or line breaks before or after it.',
    ],
    'web-html-list': [
        'Define `render_list(names)` to return an HTML string: one `<ul>` element containing one `<li>` element per name, in input order.',
        'Escape each name before placing it in the HTML. Do not add whitespace between tags.',
        'For an empty list, return `<ul></ul>`.',
    ],
    'web-attributes': [
        'Define `input_field(text)` to return an HTML string with the exact structure `<input type="text" value="...">`, replacing the dots with the supplied text.',
        'Escape special HTML characters in that value, including double quotes. Do not add other attributes or surrounding whitespace.',
    ],
    'web-query': [
        'Define `selected_region(query)`. The input is a query string such as `region=East`, without a leading question mark.',
        'Return the decoded first value of the `region` parameter as a string. Decode URL-encoded spaces.',
        'Return `"all"` if the parameter is missing or its value is blank.',
    ],
    'web-encode': [
        'Define `search_url(term)` to return a URL string beginning with `/search?` and containing one query parameter named `q`.',
        'Encode the supplied search term as that parameter’s value, so spaces, ampersands, equals signs and non-ASCII characters remain part of the term when the URL is parsed.',
    ],
    'web-url-parts': [
        'Define `report_request(url)` for either a relative URL or a complete URL.',
        'Return a dictionary with `"path"` containing the path alone, and `"region"` containing the first decoded region query value.',
        'Use `"all"` for a missing or blank region. Leave the query string and any `#fragment` out of the returned path.',
    ],
    'web-responses': [
        'Define `route(path)` to return a Python dictionary with keys `"status"`, `"headers"` and `"body"`. This exercise models a response; do not start a server.',
        'For `/api/status`, use status 200 and a JSON-string body representing an object with `"ok"` set to true.',
        'For every other path, use status 404 and a JSON-string body representing `{"error": "Not found"}`.',
        'For both cases, `"headers"` must be a dictionary whose `"Content-Type"` is `"application/json"`. The body must be encoded JSON text, not a Python dictionary.',
    ],
    'web-method': [
        'Define `route_status(method, path)` to return an integer HTTP status code. The only supported request is `GET` to `/status`.',
        'Return 404 for any unknown path, regardless of the method. For `/status`, return 200 for `GET` and 405 for any other method.',
    ],
    'web-payload': [
        'Define `parse_name(body)`, where `body` is JSON text. A valid body is an object with a string value under the `"name"` key.',
        'Return the name with surrounding whitespace removed.',
        'Raise `ValueError` for malformed JSON, a JSON value that is not an object, or a name that is missing, not a string, or blank after stripping.',
    ],
    'web-api-filter': [
        'Define `filter_sales(rows, region="all")` to return a new list of matching record dictionaries, preserving their input order.',
        'For `"all"`, include every record. Otherwise include only records whose `"region"` equals the requested region exactly.',
        'Leave the input list unchanged. Return an empty list when there are no matches or no input records.',
    ],
    'web-api-review': [
        'Define `summary_response(query, rows)`. Read the first decoded `region` query value, using `"all"` for a missing or blank value.',
        'Select all records for `"all"`; otherwise select records whose region matches exactly. Leave the input records unchanged.',
        'Return a dictionary with `"status"` equal to 200 and `"body"` containing a JSON string. Its JSON object must have `"region"` (requested region), `"count"` (matching record count), and `"total"` (sum of their revenue).',
        'For a region with no records, use zero for both count and total.',
    ],
    'web-page-1': [
        'Define `render_rows(records)`. Each record has a product `"name"` and numeric `"revenue"`.',
        'Return one combined HTML string, with a `<tr>` per record and two `<td>` cells: the escaped name first, then revenue formatted to two decimal places.',
        'Keep input order and add no whitespace between rows or tags. Return an empty string for an empty list.',
    ],
    'web-page-2': [
        'Use `records` to create a string variable named `page` containing a complete HTML document with `<html>`, `<head>` and `<body>` elements.',
        'Use `Sales report` for both the document’s `<title>` and its visible `<h1>` heading.',
        'Include a table with `<th>` headers `Product` and `Revenue`, then one row per record. Show product names and revenue amounts with two decimal places.',
        'Save the exact contents of `page` to `report.html` using UTF-8 encoding.',
    ],
    'bridge-refunds': [
        'Define `reconcile(texts)` to summarise a list of money amounts supplied as strings. Accept valid finite numbers, including refunds (negative amounts) and zero.',
        'Reject blank strings, invalid numeric text, `NaN` and infinity. Count each rejected input once.',
        'Return a dictionary with `"total"` (sum of accepted amounts, rounded to two decimals), `"accepted"` (accepted input count), and `"rejected"` (rejected input count). Use zeros for an empty list.',
    ],
    'bridge-latest': [
        'Define `latest_customers(rows)`. Each record contains `"id"`, `"updated"` (an ISO date string), and `"name"`.',
        'Return a list containing one record per customer ID: the one with the newest date. If dates tie, keep the first record with that date.',
        'Order the result by when each distinct ID first appeared in the input, not by update date. Do not modify the input records. Return an empty list for empty input.',
    ],
    'bridge-quality': [
        'Define `region_report(rows)` for records containing `"region"` and `"amount"`. Strip surrounding whitespace from region names and make them lowercase.',
        'Exclude a record if its cleaned region is blank or its amount is `None`. Include zero amounts.',
        'Return a dictionary with `"totals"` mapping each cleaned region to its combined amount, and `"excluded"` counting rejected records. Insert the totals’ keys in alphabetical order.',
        'For an empty input, return an empty totals dictionary and an excluded count of zero.',
    ],
    'bridge-contract': [
        'Define `accepts_shipping(candidate)`. Its argument is a function that you must check, not a shipping amount.',
        'Call that function with amounts 0, 49, 50 and 80. The correct shipping charges are respectively 4, 4, 0 and 0.',
        'Return `True` only if every result matches. Return `False` for any wrong result or any exception raised by the candidate.',
    ],
    'arrays-vector': [
        'Create a NumPy array named `temperatures` from `celsius`, using a floating-point data type.',
        'Create a NumPy array named `fahrenheit` containing the corresponding Fahrenheit temperature for each reading. The conversion rule is Celsius multiplied by 9/5, then increased by 32.',
        'Keep the readings in their original order.',
    ],
    'arrays-shape': [
        'The NumPy array `readings` has one row per day and one column per sensor. Create `shape` containing its shape tuple.',
        'Create `second_day` containing all readings from row index 1 as a one-dimensional array.',
        'Create `first_sensor` containing all readings from column index 0 as a one-dimensional array.',
    ],
    'arrays-axes': [
        'Each row of `readings` is a day and each column is a sensor.',
        'Create a NumPy array named `per_sensor` with one mean per sensor, across all days. Create `per_day` with one mean per day, across all sensors.',
        'Create a numeric variable named `overall` containing the mean of every reading in the array.',
    ],
    'arrays-masks': [
        'Create a NumPy array named `cleaned` containing only the finite, nonnegative entries from `values`, in their original order.',
        'Exclude negative numbers, `NaN` and infinity; retain zero. Create `rejected` containing the number of removed entries.',
    ],
    'arrays-broadcast': [
        'Each row of `units` is a day and each column is a product. The matching entry in `prices` is that product’s unit price.',
        'Create a NumPy array named `converted` with the same shape as `units`, containing the revenue for each day and product.',
        'Create a one-dimensional NumPy array named `daily_total` containing the combined product revenue for each day, in row order.',
    ],
    'arrays-sensor-project': [
        'Define `sensor_report(readings)` for a sequence of numeric sensor readings. Accept only finite values from 0 through 100, including both boundaries.',
        'Return a dictionary with `"count"` (accepted readings), `"rejected"` (removed readings), `"mean"` (accepted mean rounded to two decimals), and `"maximum"` (largest accepted reading).',
        'When no readings are accepted, use `None` for mean and maximum. An empty input has both counts equal to zero.',
    ],
    'charts-line': [
        'Create a Matplotlib figure named `fig` and an axes object named `ax` containing one line chart.',
        'Use `days` for the horizontal coordinates and `revenue` for the vertical coordinates, preserving the input pairs.',
        'Set the title to `Weekly revenue`, the x-axis label to `Day`, and the y-axis label to `Revenue`.',
    ],
    'charts-bar': [
        'Create a Matplotlib axes object named `ax` with a horizontal bar for each entry in `products`. Each bar’s width must be its corresponding `revenue`.',
        'Use the product names as the category labels in input order. Start the numeric x-axis at zero.',
        'Set the x-axis label to `Revenue` and the title to `Revenue by product`.',
    ],
    'charts-histogram': [
        'Create a Matplotlib axes object named `ax` and draw a histogram of `minutes` with bin edges `[0, 10, 20, 30]`.',
        'Save the bin counts returned by `ax.hist` in a variable named `counts`, and its returned bin edges in `edges`.',
        'Label the x-axis `Minutes` and the y-axis `Deliveries`.',
    ],
    'charts-scatter': [
        'Create a Matplotlib axes object named `ax` with a scatter plot: `spend` on the x-axis and the corresponding `revenue` on the y-axis.',
        'Create a numeric variable named `correlation` containing the Pearson correlation coefficient between those two input lists, without rounding.',
        'Label the x-axis `Ad spend` and the y-axis `Revenue`.',
    ],
    'charts-export': [
        'Create a Matplotlib axes object named `ax` with vertical bars for North revenue of 30 and South revenue of 20, in that order.',
        'Set the title to `Regional sales` and the y-axis label to `Revenue`.',
        'Save the chart as an actual PNG file named `report.png`.',
    ],
    'charts-dashboard': [
        'Create one Matplotlib figure named `fig` containing two axes objects named `trend` and `categories`.',
        'On `trend`, draw a line using days 1 through 4 on the x-axis and `daily` on the y-axis. Title it `Daily revenue`.',
        'On `categories`, draw vertical bars for Tea revenue of 40 and Cake revenue of 35. Title it `Product revenue`.',
        'Label both y-axes `Revenue` and save the complete figure to `dashboard.png`.',
    ],
    'wrangling-pivot': [
        'Reshape `df` into a DataFrame named `wide`: use month names as its row index and region names as its columns.',
        'Each cell must contain the sum of `amount` for that month and region. Combine duplicate pairs and use zero where a pair is absent.',
        'Include `North` and `South` columns and sort the month labels alphabetically.',
    ],
    'wrangling-melt': [
        'Reshape `df` into a DataFrame named `long` with one row per product and month, instead of separate month columns.',
        'Use columns `"product"`, `"month"` and `"sales"`, in that order. Each sales value belongs to its original product and month.',
        'Sort alphabetically by product and then by month label. Reset the row index to consecutive integers starting at zero.',
    ],
    'wrangling-join-audit': [
        'Define `join_orders(orders, products)` for two DataFrames with an `"id"` key column. Return a tuple `(joined, missing_ids)`.',
        '`joined` must be a left merge that preserves every order. Validate a many-to-one relationship: multiple orders may use the same product, but product IDs must be unique.',
        '`missing_ids` must be a sorted Python list of distinct order IDs with no matching product. Duplicate IDs in the products table must raise `pd.errors.MergeError`.',
    ],
    'wrangling-concat': [
        'Define `combine_exports(older, newer)` for two DataFrames containing order records keyed by `"order_id"`.',
        'Combine the older rows followed by the newer rows, retaining only the last occurrence of each order ID.',
        'Return a new DataFrame sorted by order ID with a consecutive index starting at zero. Do not modify either input DataFrame.',
    ],
    'wrangling-rolling': [
        'Create a DataFrame named `ordered` from `df`, with `"date"` parsed as dates and records ordered from earliest to latest.',
        'Add an `"average"` column containing the trailing mean of three consecutive `"amount"` values, including the current row.',
        'The first two averages must be missing because those rows do not yet have a complete three-observation window.',
    ],
    'wrangling-monthly-project': [
        'Read `transactions.csv`. Strip and lowercase region names; parse the dates and numeric amounts.',
        'Reject records with invalid dates, invalid or negative amounts, or blank cleaned regions. Keep zero amounts and count each rejected record once.',
        'Create a DataFrame named `summary` with columns `"month"`, `"region"` and `"total"`. Use `YYYY-MM` month labels, sum amounts for each month-region pair, and sort by month then region.',
        'Create a dictionary named `quality` with `"accepted"` and `"rejected"` row counts. Save the summary to `monthly.csv` without an index column, and save the dictionary to `quality.json`.',
    ],
    'excel-read': [
        'Open the provided `source.xlsx` workbook and read its `Sales` worksheet.',
        'Create a list named `rows` containing the data rows as `(product, quantity, price)` tuples, excluding the header.',
        'Create a numeric variable named `revenue` containing the combined quantity-times-unit-price amount across those rows. Close the workbook after reading.',
    ],
    'excel-write': [
        'Create a workbook file named `report.xlsx` with a worksheet named `Summary`.',
        'The first row must contain headers `Product` and `Revenue`. Follow it with Tea and numeric revenue 30, then Cake and numeric revenue 24.',
        'Save the workbook so the checks can open the file and read those cells.',
    ],
    'excel-format': [
        'Open `source.xlsx` and format its `Sales` worksheet without changing the cell values.',
        'Make all three cells in the header row bold, freeze panes at `A2`, and set column A’s width to 22.',
        'Apply number format `0.00` to the price cells in column C below the header. Save the result as `formatted.xlsx`.',
    ],
    'excel-formulas': [
        'Open the `Sales` worksheet in the provided `source.xlsx` workbook. Add the header `Revenue` in cell `D1`.',
        'In `D2` and `D3`, store Excel formulas that multiply the quantity in column B by the price in column C of the same row. Store formulas, not precomputed numbers.',
        'Separately create `python_total`, a numeric total calculated in Python from the original quantity and price cells. Do not rely on openpyxl to evaluate formulas.',
        'Save the workbook as `formulas.xlsx`.',
    ],
    'excel-validate': [
        'Read the `Dirty` worksheet in `source.xlsx`, excluding its header row.',
        'Accept a row only if its product is a nonblank string and its quantity and price are nonnegative numeric cell values. Accept zero; reject missing cells and text in numeric columns.',
        'Create `valid_rows` as a list of accepted `(product, quantity, price)` tuples in input order, stripping product names. Create `rejected` as the count of rejected data rows.',
    ],
    'excel-workbook-project': [
        'Read `sales.csv`. Strip product names and reject blank names or quantities that are invalid or negative. Accept zero quantities.',
        'Create a workbook with a `Summary` sheet: headers `Product` and `Units`, then one row per product with its total quantity, sorted alphabetically by product name.',
        'Add an `Audit` sheet: headers `Metric` and `Count`, then rows named `accepted` and `rejected` containing their input-row counts, in that order.',
        'Make the headers on both sheets bold and save the workbook as `sales_report.xlsx`.',
    ],
    'sql-select': [
        'Connect to the provided `shop.db` database and query the `customers` table.',
        'Create a list named `rows` containing one-item tuples of customer names from the `North` region, sorted alphabetically by name.',
        'Close the database connection when finished.',
    ],
    'sql-parameters': [
        'Define `find_customer(conn, name)`, where `conn` is an existing SQLite connection to `shop.db`.',
        'Query `customers` for an exact name match and return a list of `(id, name)` tuples sorted by ID.',
        'Use a parameterised query. Treat apostrophes and SQL-like text as part of the name; return an empty list when no name matches. Leave the caller’s connection open.',
    ],
    'sql-group': [
        'Query the `orders` table in `shop.db`, grouping orders by customer ID.',
        'Create a list named `totals` containing `(customer_id, total)` tuples, where total is that customer’s combined order amount. Keep only totals of at least 30.',
        'Order the results by total descending, then by customer ID ascending for ties.',
    ],
    'sql-left-join': [
        'Use `customers` and `orders` in `shop.db` to create a list named `report` containing `(name, total, order_count)` tuples.',
        'Include every customer, including those with no orders. Their total and order count must both be zero.',
        'For other customers, total is the sum of their order amounts and order count is the number of their orders. Sort the report alphabetically by customer name.',
    ],
    'sql-transaction': [
        'Define `add_orders(conn, rows)`, where `conn` is an existing SQLite connection and each input tuple contains `(id, customer_id, amount)` for the `orders` table.',
        'Insert and commit the entire batch when all amounts are valid. A negative amount must raise `ValueError`.',
        'If any record fails, leave none of that batch’s records in the database. Keep records from earlier successful batches and leave the caller’s connection open.',
    ],
    'sql-sql-project': [
        'Create a customer revenue report from `customers` and `orders` in `shop.db`.',
        'Store the results in a list named `rows`, using `(name, region, revenue, orders)` tuples. Include customers with no orders, giving them zero revenue and zero order count.',
        'Rank rows by revenue descending, then name ascending for ties. Create `grand_total` containing the sum of the report’s revenue.',
        'Write those rows to `customer_report.csv` with the header columns `name,region,revenue,orders`, in exactly that order.',
    ],
    'apis-get': [
        'Import `base_url` from the provided `practice_api` module. Define `fetch_json(url)` to request that URL and return its decoded JSON value.',
        'Use the function to request the practice API’s `/status` endpoint. Store the returned Python dictionary in a variable named `status`.',
        'Close responses after reading them. The practice API runs inside this exercise; no real server or online account is needed.',
    ],
    'apis-query': [
        'Import `base_url` and re-create the supplied `fetch_json` helper. Define `search(text)`.',
        'Request the practice API’s `/search` endpoint with the supplied text as the query parameter named `q`. Encode it so punctuation, spaces and Unicode remain part of the value.',
        'Return the string from the response’s `"query"` field, not the entire response dictionary. An empty search must return an empty string.',
    ],
    'apis-errors': [
        'Re-create the supplied `fetch_json` helper and define `optional_json(url)` to call it.',
        'Return the decoded JSON result on success. Return `None` when it raises `HTTPError` with status 404.',
        'Re-raise every other `HTTPError` so failures such as status 500 are not mistaken for missing data.',
    ],
    'apis-pages': [
        'Import `base_url`, re-create `fetch_json`, and define a function named `all_orders` that takes no arguments.',
        'Begin at `/orders`. Each response has `"items"` containing records and `"next"` containing the next relative path or `None` when there are no more pages.',
        'Return a single list containing the records from every page, preserving page order and the order within each page. Do not return only the first response.',
    ],
    'apis-retry': [
        'Re-create `fetch_json` and define `retry_json(url, attempts=3)` to return its decoded JSON result when a request succeeds.',
        'Retry only `HTTPError` status 503. The `attempts` value limits the total number of calls, including the first call. Re-raise the last error if that limit is reached.',
        'Immediately re-raise other HTTP errors. Raise `ValueError` before making any request when `attempts` is less than 1. No delay between attempts is required here.',
    ],
    'apis-report-project': [
        'Use the practice API to collect every order, starting at `/orders` and following each response’s `"next"` path until it is `None`.',
        'Calculate the number of collected records and the sum of their `"amount"` values.',
        'Save these calculated results as a JSON object in `api_report.json`, with keys `"count"` and `"total"`. Fetch the records rather than hard-coding the report.',
    ],
    'engineering-unittest': [
        'Re-create the supplied `shipping` function and define a test class named `ShippingTests` that inherits from `unittest.TestCase`.',
        'Add test methods that call `shipping` for amounts 0, 49, 50 and 80, checking charges of 4, 4, 0 and 0 respectively.',
        'Use assertions so wrong charges fail the tests. The checker will run your test class against both correct and faulty versions of `shipping`; do not start a command-line test runner.',
    ],
    'engineering-dependencies': [
        'Define `summarise(loader)`, where `loader` is a function that returns a list of numbers when called with no arguments.',
        'Call `loader` exactly once. Return a dictionary with `"count"` containing the number of returned values and `"total"` containing their sum.',
        'Include negative values and zero. For an empty list, return zero for both results.',
    ],
    'engineering-arguments': [
        'Define `options(argv)` to parse the supplied list of command-line argument strings using `argparse`.',
        'Support `--input`, whose value defaults to `sales.csv`, and a `--dry-run` flag that is false by default and true when present.',
        'Return the parsed namespace with attributes `.input` and `.dry_run`. Parse the function’s `argv` argument, not the browser process’s arguments.',
    ],
    'engineering-logging': [
        'Define `keep_nonnegative(values, logger)` to return a new list of nonnegative input numbers in their original order, including zero.',
        'Call the supplied logger’s `warning` method once for each rejected negative value. Do not warn for accepted entries or an empty input.',
    ],
    'engineering-modules': [
        'In the `calculations.py` editor tab, define `total(values)` to return the sum of its input numbers, or zero for an empty list.',
        'In `main.py`, import that function and call it with the list `[10, -2, 0]`. Store its returned value in a variable named `answer`.',
        'Keep the reusable function in `calculations.py`; the checks will import it independently.',
    ],
    'engineering-tool-project': [
        'In `cleaning.py`, define `clean_amounts(texts)` to return a list of finite numbers parsed from the input strings, in input order. Retain negative numbers and zero; omit blanks, invalid text, `NaN` and infinity.',
        'In `main.py`, import that function and use it to clean the lines from `amounts.txt`.',
        'Write `summary.json` containing `"count"` (accepted numbers) and `"total"` (their sum). Keep the cleaning function reusable for other inputs.',
    ],
    'flask-route': [
        'Create a Flask application stored in a variable named `app`.',
        'Add a route for `GET /` that returns status 200 and an HTML heading `<h1>Hello, Python!</h1>`.',
        'Do not call `app.run()`. Use Codey’s Preview app button to view the page.',
    ],
    'flask-query': [
        'Create a Flask application named `app` with a `GET /greet` route.',
        'Read the query parameter named `name`, defaulting to `"friend"` when absent.',
        'Return a JSON response with a `"message"` field containing a greeting in the format `Hello, Mei!`, using the requested name. Do not call `app.run()`.',
    ],
    'flask-templates': [
        'Create a Flask application named `app` with a `GET /` route. Read the `name` query parameter, defaulting to `"friend"` when absent.',
        'Use `render_template_string` to return an `<h1>` greeting in the format `Hello, Mei!`, using the requested name.',
        'Insert the name through template variables so HTML characters in it are escaped. Do not call `app.run()`.',
    ],
    'flask-forms': [
        'Create a Flask application named `app`. For `GET /`, show an HTML form that submits to `/` using POST and has an input named `name`.',
        'For `POST /`, strip the submitted name. Return status 400 if it is blank; otherwise redirect to `/hello` with the cleaned name in its query string.',
        'For `GET /hello`, display an escaped greeting in the format `Hello, Mei!`, using the query’s name. Do not call `app.run()`.',
    ],
    'flask-database': [
        'Create a Flask application named `app` and a SQLite database `notes.db`. Create a `notes` table with an integer primary key `id` and a text column `text`.',
        'For `POST /notes`, read the form field `text` and strip it. Return status 400 for a blank value; otherwise save it and return JSON `{"saved": true}` with status 201.',
        'For `GET /notes`, return JSON with a `"notes"` key containing a list of stored note texts in insertion order. Initially return an empty list.',
        'Use parameters for inserted text and persist changes between requests. Do not call `app.run()`.',
    ],
    'flask-tracker-project': [
        'Create a Flask application named `app` and a SQLite database `tasks.db` with a `tasks` table containing integer primary key `id` and text column `title`.',
        'For `GET /`, show an Add form with an input named `title`, followed by the saved task titles in insertion order.',
        'For `POST /`, strip the submitted title. Return status 400 if it is blank; otherwise save it to the database and redirect to `/`.',
        'Escape titles when displaying them so user-entered markup appears as text. Do not call `app.run()`; use Preview app to try the form.',
    ],
    'capstones-analysis': [
        'Build a regional sales report from `sales.csv`. Strip and lowercase region names. Reject blank regions and amounts that are invalid, nonfinite or negative; retain zero.',
        'Create `report.xlsx` with a `Summary` sheet containing columns `region` and `amount`: one row per cleaned region with its combined amount, sorted alphabetically.',
        'Create a Matplotlib axes object named `ax` showing those regional totals as vertical bars, with a meaningful title and labels on both axes. Save it to `report.png`.',
        'Write `audit.json` with `"accepted"` and `"rejected"` input-row counts. Count a rejected record only once even if it has multiple problems.',
    ],
    'capstones-automation': [
        'In `audit.py`, define `audit(texts)` to parse finite numbers from strings. Accept negative values and zero; reject blank or invalid text, `NaN` and infinity.',
        'Return a dictionary with `"count"` (accepted entries), `"rejected"` (rejected entries), and `"total"` (sum of accepted values, rounded to two decimals). Return zeros for an empty input.',
        'In `main.py`, import that function and use it on the lines of each direct `.txt` file in `inbox`, in alphabetical filename order.',
        'Write `batch.json` as a list of per-file dictionaries containing `"file"` (filename only), `"count"`, `"rejected"` and `"total"`.',
    ],
    'capstones-web': [
        'Create a Flask application named `app` and a SQLite database `inventory.db`. Create an `items` table with integer primary key `id`, text column `name`, and integer column `quantity`.',
        'For `GET /`, show an HTML form with inputs named `name` and `quantity`, followed by stored records in insertion order.',
        'For `POST /`, accept only a stripped nonblank name and an integer quantity of zero or more. Return status 400 for blank names, negative quantities, decimal text or invalid integer text.',
        'Persist a valid record, then redirect to `/`. Escape names when displaying them. Do not call `app.run()`.',
    ],
}


def clarify_briefs(modules):
    for module in modules:
        for task in module['tasks']:
            if task['id'] in BRIEFS:
                task['goal'] = BRIEFS[task['id']]
            console_checked = any('__output__' in check['code'] for check in task['checks'])
            task['submission_note'] = (
                'Print only the result requested above. The checks also read your console output.'
                if console_checked else
                'You do not need to print anything. Submit the variables, functions, files or app behavior requested above.'
            )
            if task['id'].startswith('sql-'):
                task['provided_resources'] = [{
                    'name': 'shop.db',
                    'description': 'A SQLite database is ready to use. In `orders`, `customer_id` refers to `customers.id`. Both `id` columns are integer primary keys; names and regions are text, and amounts are numbers.',
                    'preview': 'customers\nid | name | region\n1  | Ari  | North\n2  | Bo   | South\n3  | Cy   | North\n\norders\nid | customer_id | amount\n1  | 1           | 10\n2  | 1           | 20\n3  | 2           | 40',
                }]
            if task['id'] in {'excel-read', 'excel-format', 'excel-formulas', 'excel-validate'}:
                dirty = task['id'] == 'excel-validate'
                task['provided_resources'] = [{
                    'name': 'source.xlsx',
                    'description': ('Worksheet `Dirty` has columns `Product`, `Qty` and `Price`. `None` below means a blank cell. Spaces inside quoted names are part of the data.' if dirty else
                                    'Worksheet `Sales` has columns `Product`, `Qty` and `Price`, in that order.'),
                    'preview': ('Product  | Qty    | Price\n" Tea "  | 2      | 5\nCake     | 0      | 8\nCoffee   | "many" | 4\nNone     | 2      | 3\nJuice    | -1     | 5' if dirty else
                                'Product | Qty | Price\nTea     | 2   | 5\nCake    | 3   | 8'),
                }]
            if task['id'] == 'apis-get':
                task['concept'] = ('An API returns structured data over HTTP. Open a response inside a with block so the connection closes. '
                                   '`json.load` reads the response and decodes its JSON. Codey provides an offline practice API in browser Python. '
                                   'Import `base_url` from `practice_api` to build its request URLs; no online account is needed.')
