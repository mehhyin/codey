"""Original practice sequences. Existing IDs are kept so saved work survives expansion."""


def expand(modules, task):
    by_id = {m['id']: m for m in modules}
    insertions = {}

    def add(mid, after, slug, title, concept, example, goals, starter, solution,
            checks, hints, explanation, walkthrough, pitfall, kind='practice', minutes=12, files=None):
        m = by_id[mid]
        task(m, slug, title, concept, example, goals, starter, solution, checks, hints,
             explanation, kind=kind, minutes=minutes, files=files)
        item = m['tasks'].pop()
        item['walkthrough'] = walkthrough
        item['pitfall'] = pitfall
        insertions.setdefault((mid, after), []).append(item)

    add('basics', 'variables', 'types', 'Numbers and text are different',
        'Two values can look alike but behave differently. 7 is an integer; "7" is a string. Adding numbers performs arithmetic, while adding strings joins their characters. type(value).__name__ tells you the type as readable text. Before running the example, predict whether its first line prints 14 or 77. Then inspect the types to explain the difference. You will meet this issue repeatedly when reading CSV files.',
        'print("7" + "7")  # 77\nprint(7 + 7)      # 14\nprint(type(7).__name__)  # int',
        ['Create `joined` by adding the two text values. Create `added` by adding the numeric values.', 'Set `text_type` and `number_type` to the readable type names of `joined` and `added`.'],
        'left_text = "12"\nright_text = "3"\nleft_number = 12\nright_number = 3\n',
        'left_text = "12"\nright_text = "3"\nleft_number = 12\nright_number = 3\njoined = left_text + right_text\nadded = left_number + right_number\ntext_type = type(joined).__name__\nnumber_type = type(added).__name__',
        [('Join text', 'assert joined == "123"'), ('Add numbers', 'assert added == 15'), ('Inspect the types', 'assert text_type == "str" and number_type == "int"')],
        ['Quotation marks make a value text.', 'Use + in both expressions and compare what it does.', 'type(joined).__name__ produces "str". Repeat for added.'],
        'The operator is the same, but the operand types determine its behavior. Conversion is a separate decision; Python does not silently turn numeric-looking strings into numbers.',
        ['"7" + "7" joins two strings; it never converts them.', '7 + 7 adds two integers and returns an integer.', '__name__ extracts the type name for display.'],
        'A string containing digits is still a string. Its appearance does not make it numeric.')
    add('basics', 'variables', 'precedence', 'Control the calculation order',
        'Python performs multiplication and division before addition and subtraction. Parentheses let you express a different order. In a bill, a fee charged per item differs from a fee charged once per order. Translate the rule into a small calculation before typing it. You can print intermediate values when the final total is surprising; this is often easier than staring at one long expression.',
        'print(10 + 2 * 3)    # 16\nprint((10 + 2) * 3)  # 36',
        ['Calculate `per_item_total` when each item costs 8 plus a 2 handling fee, for 3 items.', 'Calculate `per_order_total` when 3 items cost 8 each, with one 2 handling fee.'],
        'price = 8\nfee = 2\nquantity = 3\n',
        'price = 8\nfee = 2\nquantity = 3\nper_item_total = (price + fee) * quantity\nper_order_total = price * quantity + fee',
        [('Apply the fee per item', 'assert per_item_total == 30'), ('Apply the fee once per order', 'assert per_order_total == 26')],
        ['Ask which amount is being multiplied by quantity.', 'For a per-item fee, group price + fee with parentheses.', 'The per-order fee is added after multiplying price by quantity.'],
        'Parentheses encode the business rule. Both formulas are valid Python, so a syntax check alone cannot tell you which calculation you intended.',
        ['2 * 3 happens before adding 10 in the first expression.', 'Parentheses force 10 + 2 to happen first in the second.', 'A correct calculation must match the meaning of the inputs.'],
        'A program can run without errors while implementing the wrong rule.')
    add('basics', 'variables', 'division', 'Split a quantity into groups',
        'Use / for ordinary division, // for floor division, and % for the remainder. For nonnegative quantities, floor division counts complete groups and the remainder counts leftovers. These operators help with pagination, packing, and time conversion. The remainder always relates to the divisor: with groups of five, the leftover count is between zero and four. Here all inputs are positive.',
        'print(17 / 5)   # 3.4\nprint(17 // 5)  # 3 complete groups\nprint(17 % 5)   # 2 left over',
        ['There are 53 photos and space for 8 photos per page.', 'Calculate `full_pages`, `leftover_photos`, and `average_pages` using `//`, `%`, and `/`.'],
        'photos = 53\nper_page = 8\n',
        'photos = 53\nper_page = 8\nfull_pages = photos // per_page\nleftover_photos = photos % per_page\naverage_pages = photos / per_page',
        [('Count complete pages', 'assert full_pages == 6'), ('Find the leftovers', 'assert leftover_photos == 5'), ('Calculate ordinary division', 'assert average_pages == 6.625')],
        ['Six full pages hold 48 photos.', '// gives complete groups, while % gives leftovers.', 'Use / for average_pages; do not round it.'],
        'The identity full_pages * per_page + leftover_photos reconstructs 53. Use that relationship to check your own calculation.',
        ['17 / 5 keeps the fractional part.', '17 // 5 counts three complete groups for these positive inputs.', '17 % 5 is what remains after those groups are removed.'],
        'Floor division rounds downward; for negative inputs this differs from truncating toward zero.')
    add('basics', 'variables', 'updates', 'Trace a changing variable',
        'Assignment happens immediately, in order from top to bottom. A variable stores the result at that moment; it does not remember a formula that updates automatically. Writing balance = balance - purchase reads the old balance, computes a new number, then stores the result back under the same name. The shorthand balance -= purchase does the same update. Trace each line before running it.',
        'balance = 30\nprevious = balance\nbalance -= 8\nprint(previous, balance)  # 30 22',
        ['Start with the provided `balance` of 100 and save it in `opening`.', 'Subtract a purchase of 25, then add a refund of 7.', 'Set `closing` to the final `balance`. `opening` should still be 100.'],
        'balance = 100\n',
        'balance = 100\nopening = balance\nbalance -= 25\nbalance += 7\nclosing = balance',
        [('Keep the opening value', 'assert opening == 100'), ('Apply updates in order', 'assert closing == 82 and balance == 82')],
        ['Save opening before changing balance.', 'Subtract 25, then add 7.', 'Copy the final balance to closing.'],
        'The integer assigned to opening stays 100. Updating balance rebinds that name; it does not retroactively change opening.',
        ['previous receives 30 when its assignment runs.', 'The subtraction creates 22 and assigns it to balance.', 'Printing both names shows the old snapshot and current value.'],
        'An assignment such as total = price * quantity is not a live spreadsheet formula.')
    add('basics', 'strings', 'text-methods', 'Clean a label before displaying it',
        'A string method is a named operation called with a dot. strip() removes whitespace at the beginning and end, lower() changes letter case, and replace(old, new) substitutes matching text. Strings are immutable: methods return new strings instead of changing the original. Chain methods when the order is easy to follow, or store intermediate values to inspect each step.',
        'raw = "  GREEN TEA  "\nclean = raw.strip().lower()\nprint(clean)  # green tea\nprint(raw)    # original is unchanged',
        ['Create `cleaned` by stripping `raw`, lowercasing it, and replacing spaces with underscores.', 'Leave `raw` unchanged.'],
        'raw = "  Monthly Sales  "\n',
        'raw = "  Monthly Sales  "\ncleaned = raw.strip().lower().replace(" ", "_")',
        [('Create a consistent label', 'assert cleaned == "monthly_sales"'), ('Preserve the raw input', 'assert raw == "  Monthly Sales  "')],
        ['Remove the outer whitespace before replacing inner spaces.', 'Chain .strip().lower().', 'Finish with .replace(" ", "_").'],
        'The result is a consistent machine-friendly label. The original value stays available for auditing or display.',
        ['strip() removes the outer spaces, not the space between GREEN and TEA.', 'lower() returns lowercase text.', 'Assigning the result keeps it available under a new name.'],
        'Calling raw.strip() without assigning its result leaves raw unchanged.')
    add('basics', 'strings', 'split-join', 'Separate and rebuild text',
        'split(separator) divides a string and returns a list of parts. A list is an ordered container written with square brackets. join() does the reverse: call it on the separator you want between the parts. This is useful for simple labels, but use the csv module for real CSV files because quoted fields can contain commas of their own.',
        'parts = "red|green|blue".split("|")\nprint(parts[0])             # red\nprint(" / ".join(parts))    # red / green / blue',
        ['Split `raw` on the `|` character into `parts`.', 'Create `display` by joining those `parts` with `" → "`.', 'Set `first` to the first part using index 0.'],
        'raw = "load|clean|report"\n',
        'raw = "load|clean|report"\nparts = raw.split("|")\ndisplay = " → ".join(parts)\nfirst = parts[0]',
        [('Split into three parts', 'assert parts == ["load", "clean", "report"]'), ('Join with a new separator', 'assert display == "load → clean → report"'), ('Read the first part', 'assert first == "load"')],
        ['The separator in the original text is |.', 'Call join on the new separator string.', 'Python uses index 0 for the first item.'],
        'Splitting exposes individual pieces; joining formats them for display. The delimiter determines where one piece ends and the next begins.',
        ['split("|") returns three strings in a list.', 'parts[0] selects the first string.', '" / ".join(parts) inserts the separator only between parts.'],
        'join expects strings. Convert numbers before trying to join them.')
    add('basics', 'conversion', 'debug-types', 'Repair a calculation that runs',
        'Some bugs do not raise exceptions. Multiplying a string by an integer repeats the string, so "5" * 3 produces "555". When an output looks wrong, check the types before changing the arithmetic. This exercise deliberately contains a working but incorrect line. Run it once to observe the symptom, then repair the type conversion at the input boundary.',
        'print("4" * 2)       # 44\nprint(float("4") * 2)  # 8.0',
        ['Fix `total` so it is the numeric cost of `quantity` items at `price_text` each.', 'Print the numeric `total`. Keep the original inputs.'],
        'price_text = "6.25"\nquantity = 3\ntotal = price_text * quantity\nprint(total)\n',
        'price_text = "6.25"\nquantity = 3\ntotal = float(price_text) * quantity\nprint(total)',
        [('Calculate a number, not repeated text', 'assert isinstance(total, (int, float)) and total == 18.75'), ('Display the numeric result', 'assert __output__.strip() == "18.75"')],
        ['Inspect the type of price_text.', 'The conversion should happen before multiplication.', 'Replace price_text in the calculation with float(price_text).'],
        'You fixed a logic bug by changing the data type, not the operator. The same reasoning applies when numeric CSV columns arrive as strings.',
        ['A string times an integer repeats characters.', 'float() converts valid decimal text into a number.', 'Multiplication then performs numeric arithmetic.'],
        'A successful run only proves that Python could execute the code, not that its answer is meaningful.', kind='debug')
    add('basics', 'conversion', 'receipt-review', 'Checkpoint · split a restaurant bill',
        'Combine conversion, arithmetic, and formatting in a fresh scenario. Four friends share food and a fixed service charge. Keep calculations numeric until the final message. A checkpoint has fewer prompts so you can find out what you remember. First write down the calculation in words, then turn each part into a named value. Use the reference or hints if you need a reminder.',
        'amount = 19.5\nprint(f"Each: {amount:.2f}")  # Each: 19.50',
        ['Convert `food_text` to a number. Add `service`, then divide the total equally among `people`.', 'Store the per-person amount in `each`.', 'Create `message` exactly as `"Each person pays 24.50"` using `each`.'],
        'food_text = "90.00"\nservice = 8\npeople = 4\n',
        'food_text = "90.00"\nservice = 8\npeople = 4\nfood = float(food_text)\neach = (food + service) / people\nmessage = f"Each person pays {each:.2f}"',
        [('Share the complete bill', 'assert each == 24.5'), ('Format two decimal places', 'assert message == "Each person pays 24.50"')],
        ['Convert food_text before adding service.', 'Use parentheses so the whole bill is divided.', 'Use :.2f in the final f-string.'],
        'You combined three skills without a line-by-line template. If it was difficult, revisit conversion and calculation order before the trip project.',
        ['The value is numeric during calculations.', ':.2f creates exactly two decimal places for display.', 'Formatting is the last step, after the amount is settled.'],
        'Dividing only the food and then adding the entire service charge would charge every person the full fee.', kind='checkpoint', minutes=18)

    add('flow', 'conditions', 'boundary', 'Practice the exact boundary',
        'A threshold has three interesting cases: below it, exactly equal to it, and above it. > excludes equality while >= includes it. Test those cases deliberately. An elif chain chooses the first matching branch, so put a more specific range before a broader one. In this exercise, use separate comparisons to inspect the conditions before turning them into branches.',
        'score = 70\nprint(score > 70)   # False\nprint(score >= 70)  # True',
        ['For `score = 70`, create `above` using `score > 70` and `qualifies` using `score >= 70`.', 'Set `different` to whether `score` differs from 70, using `!=`.'],
        'score = 70\n',
        'score = 70\nabove = score > 70\nqualifies = score >= 70\ndifferent = score != 70',
        [('Distinguish > from >=', 'assert above is False and qualifies is True'), ('Test inequality', 'assert different is False')],
        ['Boolean results are True or False, without quotes.', 'Exactly 70 satisfies >= 70 but not > 70.', '!= means not equal.'],
        'Boundary tests expose mistakes that ordinary mid-range values miss. Build this habit before writing more complicated conditions.',
        ['score is exactly the threshold.', 'The strict comparison excludes it.', 'The inclusive comparison accepts it.'], 'Do not use = in place of == when comparing values.')
    add('flow', 'conditions', 'boolean', 'Combine conditions clearly',
        'and requires both conditions to be true; or requires at least one; not reverses a truth value. Name complex checks so their meaning remains visible. Parentheses can clarify how conditions belong together, even when Python would evaluate them correctly without the parentheses. Here a discount needs both membership and a minimum spend, while delivery is allowed when either pickup is selected or an address is present.',
        'member = True\nspend = 40\neligible = member and spend >= 30\nprint(eligible)  # True',
        ['Set `discount_allowed` when `member` is true and `spend` is at least 50.', 'Set `can_fulfil` when `pickup` is true or `has_address` is true.', 'Set `needs_address` when `pickup` is false and `has_address` is false.'],
        'member = True\nspend = 45\npickup = True\nhas_address = False\n',
        'member = True\nspend = 45\npickup = True\nhas_address = False\ndiscount_allowed = member and spend >= 50\ncan_fulfil = pickup or has_address\nneeds_address = not pickup and not has_address',
        [('Require both discount conditions', 'assert discount_allowed is False'), ('Accept either fulfilment option', 'assert can_fulfil is True'), ('Identify missing delivery information', 'assert needs_address is False')],
        ['Use and for the discount.', 'Use or for the two fulfilment options.', 'Negate each condition with not for needs_address.'],
        'Naming a Boolean makes a rule readable at its point of use. You can print the component conditions separately when a combined rule behaves unexpectedly.',
        ['The membership flag is already Boolean.', 'spend >= 30 produces another Boolean.', 'and combines the two into one result.'], 'The text "False" is a nonempty string, not the Boolean False.')
    add('flow', 'for', 'range', 'Generate a sequence with range',
        'range(start, stop, step) describes a sequence of integers. It includes start and excludes stop. Omitting start begins at zero; omitting step uses one. This convention fits list indices: a list of length five has positions zero through four. Use a range when you need a numeric progression rather than iterating through an existing collection.',
        'print(list(range(1, 5)))     # [1, 2, 3, 4]\nprint(list(range(2, 9, 2)))  # [2, 4, 6, 8]',
        ['Create `evens` containing 2, 4, 6, 8, and 10 using `range()`.', 'Calculate `total` by adding those values.'],
        '# Build the sequence, then calculate its total.\n',
        'evens = list(range(2, 11, 2))\ntotal = 0\nfor number in evens:\n    total += number',
        [('Include 10 as the final even number', 'assert evens == [2, 4, 6, 8, 10]'), ('Add the sequence', 'assert total == 30')],
        ['Start at 2 and step by 2.', 'The stop must be greater than 10 because it is excluded.', 'list(range(2, 11, 2)) materialises the values.'],
        'The excluded endpoint is the main detail to remember. Try printing a short range before using it in a larger calculation.',
        ['range(1, 5) stops before 5.', 'A step of 2 skips alternate integers.', 'list() displays all the generated values.'], 'range(2, 10, 2) stops at 8, not 10.')
    add('flow', 'for', 'while', 'Repeat until a condition changes',
        'A while loop checks its condition before each iteration. It repeats until that condition becomes false. Unlike a for loop over a known sequence, you are responsible for updating the state that controls it. Trace the changing value on paper first. If it never moves toward the stopping condition, the program will keep running until the practice time limit stops it.',
        'balance = 0\nweeks = 0\nwhile balance < 30:\n    balance += 10\n    weeks += 1\nprint(weeks)  # 3',
        ['Start `savings` at 20. Add 15 each week until `savings` reaches at least 80.', 'Use a `while` loop and store the number of additions in `weeks`.'],
        'savings = 20\nweeks = 0\n',
        'savings = 20\nweeks = 0\nwhile savings < 80:\n    savings += 15\n    weeks += 1',
        [('Reach the target', 'assert savings == 80'), ('Count four weeks', 'assert weeks == 4'), ('Practice a while loop', 'import ast\nassert any(isinstance(n, ast.While) for n in ast.walk(ast.parse(open("main.py").read())))')],
        ['Continue while savings is below 80.', 'Update savings and weeks inside the loop.', 'Use < rather than <= so you stop exactly at the target.'],
        'The values are 20, 35, 50, 65, and 80. Four additions occur; the initial value is not a week of saving.',
        ['The condition is checked before adding money.', 'Each iteration changes both the balance and the counter.', 'Once the balance is 30, the next condition check is false.'], 'Forgetting to update the condition variable can create an endless loop.')
    add('flow', 'filter', 'break', 'Stop when you find a match',
        'break exits the nearest enclosing loop immediately. This is useful when you need the first match rather than every match. Start with a meaningful default so the result is defined even if no match exists. Here None means no matching item has been found. After the loop, code can inspect that value instead of assuming a match was present.',
        'first = None\nfor value in [2, 9, 12]:\n    if value > 5:\n        first = value\n        break\nprint(first)  # 9',
        ['Find the first temperature above 30 and store it in `first_hot`.', 'Stop searching at that first match.'],
        'temperatures = [22, 28, 33, 31, 29]\nfirst_hot = None\n',
        'temperatures = [22, 28, 33, 31, 29]\nfirst_hot = None\nfor temperature in temperatures:\n    if temperature > 30:\n        first_hot = temperature\n        break',
        [('Keep the first match', 'assert first_hot == 33'), ('Practice early stopping', 'import ast\nassert any(isinstance(n, ast.Break) for n in ast.walk(ast.parse(open("main.py").read())))')],
        ['Check each temperature in order.', 'Assign first_hot inside the matching if block.', 'Place break immediately after that assignment.'],
        'Without break, assigning on every match would leave the last hot value, 31. Early stopping preserves the first match.',
        ['None gives the result a defined no-match state.', 'The first qualifying value is assigned.', 'break prevents later values from replacing it.'], 'break affects only the loop it is inside, not the whole program.')
    add('flow', 'filter', 'enumerate', 'Keep the position with the value',
        'enumerate(sequence) yields an index and a value together. Its optional start argument changes the counter’s initial value. A day number in a report often starts at one even though a Python list index starts at zero. Unpacking the pair into two names makes it clear which number is the position and which is the measurement.',
        'for day, amount in enumerate([12, 40], start=1):\n    print(day, amount)  # 1 12, then 2 40',
        ['Create `alert_days` containing the one-based day numbers whose spending exceeds 30.', 'Preserve chronological order.'],
        'spending = [12, 45, 18, 32, 9]\nalert_days = []\n',
        'spending = [12, 45, 18, 32, 9]\nalert_days = []\nfor day, amount in enumerate(spending, start=1):\n    if amount > 30:\n        alert_days.append(day)',
        [('Record day numbers, not amounts', 'assert alert_days == [2, 4]')],
        ['Use enumerate(spending, start=1).', 'Compare amount to the threshold.', 'Append day rather than amount.'],
        'Keeping the position makes the result actionable: you know which days to investigate instead of only knowing their spending amounts.',
        ['enumerate pairs each item with a counter.', 'start=1 creates report-friendly day numbers.', 'Both names change on every iteration.'], 'Appending the amount answers a different question from appending the day number.')
    add('flow', 'filter', 'debug-total', 'Repair an accumulator',
        'Indentation decides which statements repeat. An accumulator must be initialised before a loop if it is meant to preserve results between iterations. Resetting it inside the loop destroys earlier work. This bug is easier to understand by tracing just two iterations: observe total before and after the second reset. Repair the structure while keeping the loop.',
        'total = 0\nfor number in [2, 3]:\n    total += number\nprint(total)  # 5',
        ['Fix the code so `total` contains the sum of all `values`.', 'Print the final `total` once, after the loop.'],
        'values = [5, 8, 12]\nfor value in values:\n    total = 0\n    total += value\nprint(total)\n',
        'values = [5, 8, 12]\ntotal = 0\nfor value in values:\n    total += value\nprint(total)',
        [('Preserve earlier additions', 'assert total == 25'), ('Print once after the loop', 'assert __output__.strip() == "25"')],
        ['Which line should run once instead of repeatedly?', 'Move total = 0 above the for statement.', 'Keep total += value inside the loop and print outside it.'],
        'The repaired loop preserves its accumulated state. This pattern appears again in grouped totals, frequency counts, and automation summaries.',
        ['Initialisation happens once.', 'Only the addition repeats.', 'The final print runs after all values have contributed.'], 'A variable can have the right name and still be reset at the wrong time.', kind='debug')
    add('flow', 'filter', 'stock-review', 'Checkpoint · classify stock levels',
        'A stock report needs both a classification for every product and a list of urgent restocks. Combine branching, looping, and accumulation. Define the boundaries before writing code: zero means out, one through four means low, and five or more means healthy. A checkpoint asks you to translate those rules yourself rather than copy a completed loop.',
        'labels = []\nlabels.append("low")\nprint(labels)  # ["low"]',
        ['Create `labels` in input order: `"out"` for 0, `"low"` for 1–4, `"healthy"` for 5 or more.', 'Set `urgent_count` to the number of `quantities` below 5.'],
        'quantities = [0, 4, 5, 12, 1]\n',
        'quantities = [0, 4, 5, 12, 1]\nlabels = []\nurgent_count = 0\nfor quantity in quantities:\n    if quantity == 0:\n        labels.append("out")\n    elif quantity < 5:\n        labels.append("low")\n    else:\n        labels.append("healthy")\n    if quantity < 5:\n        urgent_count += 1',
        [('Classify boundary values', 'assert labels == ["out", "low", "healthy", "healthy", "low"]'), ('Count urgent products', 'assert urgent_count == 3')],
        ['Check zero before the broader less-than-five case.', 'Append one label on every iteration.', 'Increment urgent_count for both out and low stock.'],
        'The zero case is more specific than quantity < 5, so it comes first. The separate counter combines two labels under one action.',
        ['A list starts empty.', 'append adds a classification to its end.', 'A loop can repeat that operation once per record.'], 'If quantity < 5 is checked first, zero will be labelled low instead of out.', kind='checkpoint', minutes=18)

    add('collections', 'lists', 'slices', 'Take a window of observations',
        'A slice uses start:stop, with the stop excluded. Leaving a boundary blank uses the beginning or end. Negative indices count from the end. Slicing creates a new list, so selecting a window does not remove anything from the source. These operations are useful for taking the first rows of a dataset or reviewing its most recent observations.',
        'values = [10, 20, 30, 40, 50]\nprint(values[1:4])  # [20, 30, 40]\nprint(values[-2:])  # [40, 50]',
        ['Set `first_three` to the first three `observations`.', 'Set `last_two` to the final two `observations`.', 'Set `middle` to `observations` at indices 1 through 3 inclusive.'],
        'observations = [11, 14, 18, 20, 25, 30]\n',
        'observations = [11, 14, 18, 20, 25, 30]\nfirst_three = observations[:3]\nlast_two = observations[-2:]\nmiddle = observations[1:4]',
        [('Select the beginning', 'assert first_three == [11, 14, 18]'), ('Select the end', 'assert last_two == [25, 30]'), ('Use an exclusive stop', 'assert middle == [14, 18, 20]')],
        ['The first three positions are 0, 1, and 2.', 'Use -2 as the start to take the last two.', 'To include index 3, use stop index 4.'],
        'The selected window has stop - start items for an ordinary in-bounds slice. That relationship helps you check off-by-one mistakes.',
        ['Index 1 is the second item.', 'Stop 4 excludes the item at index 4.', 'A negative start measures backward from the end.'], 'An inclusive English phrase such as “through index 3” needs an exclusive Python stop of 4.')
    add('collections', 'lists', 'mutations', 'Update a list deliberately',
        'append adds one item, extend adds every item from another sequence, and pop removes and returns an item. With no argument, pop removes the last item. These methods change the existing list. Compare them with sorted(), which returns a new list. Watch the list after each operation to understand how the state changes.',
        'queue = ["read"]\nqueue.append("clean")\nqueue.extend(["check", "save"])\nlast = queue.pop()  # save',
        ['Append `"clean"` to `steps`, then extend it with `["analyse", "export"]`.', 'Pop the last item into `postponed`. Keep the remaining `steps`.'],
        'steps = ["load"]\n',
        'steps = ["load"]\nsteps.append("clean")\nsteps.extend(["analyse", "export"])\npostponed = steps.pop()',
        [('Update the sequence', 'assert steps == ["load", "clean", "analyse"]'), ('Keep the removed value', 'assert postponed == "export"')],
        ['append takes a single item.', 'extend adds both strings from the supplied list.', 'pop returns the removed last item.'],
        'The list now represents the remaining steps, and postponed records the item you removed. Mutation is useful when the change itself is intended.',
        ['append adds one new element.', 'extend visits the supplied sequence.', 'pop both changes the list and returns a value.'], 'append(["a", "b"]) adds a nested list; extend(["a", "b"]) adds two strings.')
    add('collections', 'lists', 'copies', 'Avoid changing the original by accident',
        'Assigning a list to another name does not copy it: both names refer to the same list. A change made through either name is visible through both. Use .copy() for an independent shallow copy when the elements are simple values. Nested lists need more care because a shallow copy still refers to the original inner objects.',
        'source = [1, 2]\nalias = source\ncopy = source.copy()\ncopy.append(3)\nprint(source)  # [1, 2]',
        ['Create `revised` as an independent copy of `original`.', 'Change the first item in `revised` to 99 and append 40.', 'Keep `original` unchanged.'],
        'original = [10, 20, 30]\n',
        'original = [10, 20, 30]\nrevised = original.copy()\nrevised[0] = 99\nrevised.append(40)',
        [('Update the copy', 'assert revised == [99, 20, 30, 40]'), ('Preserve the source', 'assert original == [10, 20, 30] and revised is not original')],
        ['Use original.copy(), not just original.', 'Assign the first item using index 0.', 'Append 40 to the copied list.'],
        'The two list objects can now change independently. Keeping a raw input and a cleaned copy is often useful in data preparation.',
        ['alias and source refer to the same object.', 'copy() creates a new outer list.', 'Appending to the copy leaves source unchanged.'], 'A shallow copy is sufficient here because the elements are numbers, not nested mutable objects.')
    add('collections', 'dicts', 'sets', 'Find what is missing',
        'A set holds unique values and supports operations such as intersection and difference. expected - received finds values that were expected but did not arrive. Set operations discard duplicates and do not preserve a display order. Sort the result when presenting it to a person, while retaining sets for membership checks and comparisons.',
        'expected = {"a.csv", "b.csv"}\nreceived = {"b.csv", "c.csv"}\nprint(sorted(expected - received))  # ["a.csv"]',
        ['Set `missing` to the `expected` filenames not `received`.', 'Set `unexpected` to `received` filenames that were not `expected`.', 'Set `shared` to filenames present in both sets. Return sets, not lists.'],
        'expected = {"sales.csv", "costs.csv", "stock.csv"}\nreceived = {"sales.csv", "notes.txt", "stock.csv"}\n',
        'expected = {"sales.csv", "costs.csv", "stock.csv"}\nreceived = {"sales.csv", "notes.txt", "stock.csv"}\nmissing = expected - received\nunexpected = received - expected\nshared = expected & received',
        [('Find the missing input', 'assert missing == {"costs.csv"}'), ('Find the unexpected file', 'assert unexpected == {"notes.txt"}'), ('Find the shared files', 'assert shared == {"sales.csv", "stock.csv"}')],
        ['Difference is directional.', 'Use received - expected for unexpected values.', 'Use & for intersection.'],
        'Set comparisons make file audits and record reconciliation concise. Sorting is only needed when a stable presentation order matters.',
        ['The left-hand set is the starting collection.', 'Difference removes values found on the right.', 'sorted converts the remaining values into an ordered list.'], 'expected - received and received - expected answer opposite questions.')
    add('collections', 'dicts', 'items', 'Visit keys and values together',
        'Dictionary iteration normally yields keys. .values() yields values, while .items() yields key-value pairs that can be unpacked into two names. Choose the view that matches your question. To calculate inventory value, you need each product name to find its price and its quantity to calculate the line value.',
        'stock = {"tea": 3, "cake": 2}\nfor name, quantity in stock.items():\n    print(name, quantity)',
        ['Create `values` mapping each item to its quantity in `stock` multiplied by its unit price in `prices`.', 'Set `inventory_value` to the sum of those `values`.'],
        'stock = {"tea": 3, "cake": 2}\nprices = {"tea": 5, "cake": 12}\n',
        'stock = {"tea": 3, "cake": 2}\nprices = {"tea": 5, "cake": 12}\nvalues = {}\nfor name, quantity in stock.items():\n    values[name] = quantity * prices[name]\ninventory_value = sum(values.values())',
        [('Calculate product values', 'assert values == {"tea": 15, "cake": 24}'), ('Sum the complete inventory', 'assert inventory_value == 39')],
        ['Iterate over stock.items().', 'Use each name to look up prices[name].', 'Sum values.values(), not the product-name keys.'],
        'The shared product key connects two dictionaries. Later, a table join will perform a similar connection between datasets.',
        ['items() supplies both the label and measurement.', 'Unpacking gives each part a readable name.', 'The key can look up related information elsewhere.'], 'sum(dictionary) tries to add its keys, which is usually not the measurement you want.')
    add('collections', 'comprehensions', 'frequency', 'Build a frequency table',
        'A frequency table counts how often each category appears. Unlike summing a measurement, each record contributes one. Normalise text before counting so differently capitalised versions of the same label do not become separate categories. get(key, 0) provides the initial count for a category you have not seen before.',
        'counts = {}\nfor label in ["a", "b", "a"]:\n    counts[label] = counts.get(label, 0) + 1\nprint(counts)  # {"a": 2, "b": 1}',
        ['Strip and lowercase each channel, excluding blanks.', 'Create `counts` with the frequency of each cleaned `channel`.'],
        'channels = [" Email ", "web", "EMAIL", "", " Web", "store"]\n',
        'channels = [" Email ", "web", "EMAIL", "", " Web", "store"]\ncounts = {}\nfor channel in channels:\n    label = channel.strip().lower()\n    if label:\n        counts[label] = counts.get(label, 0) + 1',
        [('Count normalised categories', 'assert counts == {"email": 2, "web": 2, "store": 1}')],
        ['Clean each string before looking it up.', 'Skip the cleaned empty string.', 'Increment the stored count with get(label, 0) + 1.'],
        'The category counts add to five because one blank observation was excluded. Reconcile totals when checking your own frequency table.',
        ['A new label begins with zero.', 'Every observation adds exactly one.', 'Repeated labels update an existing key.'], 'Deduplicating first would destroy the frequencies you are trying to measure.')
    add('collections', 'comprehensions', 'nested', 'Navigate nested records',
        'Records can contain other records or lists. Read nested data one level at a time: record["customer"]["city"] first selects the customer dictionary, then its city. When a path becomes hard to read, assign its intermediate object to a meaningful name. A missing key at any level can raise KeyError, so know the expected schema before navigating it.',
        'order = {"customer": {"city": "Oslo"}, "items": ["tea", "cake"]}\nprint(order["customer"]["city"])  # Oslo\nprint(len(order["items"]))         # 2',
        ['Set `city` to the customer city.', 'Calculate `units` as the sum of `qty` across all items.', 'Set `first_product` to the name of the first item.'],
        'order = {"customer": {"name": "Ari", "city": "Penang"}, "items": [{"name": "Tea", "qty": 2}, {"name": "Cake", "qty": 1}]}\n',
        'order = {"customer": {"name": "Ari", "city": "Penang"}, "items": [{"name": "Tea", "qty": 2}, {"name": "Cake", "qty": 1}]}\ncity = order["customer"]["city"]\nunits = sum(item["qty"] for item in order["items"])\nfirst_product = order["items"][0]["name"]',
        [('Read the nested customer', 'assert city == "Penang"'), ('Add item quantities', 'assert units == 3'), ('Read the first product', 'assert first_product == "Tea"')],
        ['customer is a dictionary inside order.', 'items is a list of dictionaries.', 'Select items, then index 0, then the name key.'],
        'This shape is common in JSON APIs. Identifying the type at each level helps you choose a key, an index, or a loop.',
        ['The first lookup returns a dictionary.', 'The second lookup reads a value inside it.', 'The items field uses list operations instead.'], 'A dictionary key and a list index are different kinds of lookup, even though both use square brackets.')
    add('collections', 'comprehensions', 'restock-review', 'Checkpoint · prepare a restock list',
        'Combine record filtering, calculations, and ordering. A shop wants to bring low-stock products up to a target quantity. A restock list should contain only products below target, with the number of units to buy. Keep the input records unchanged so the plan can be reviewed against the original stock report.',
        'rows = [{"name": "Tea", "buy": 2}]\nordered = sorted(rows, key=lambda row: row["name"])',
        ['Build `restock` for `products` with `stock` below `target`, using dictionaries with `name` and `buy`.', '`buy` is `target` minus `stock`. Sort `restock` alphabetically by `name`.', 'Leave `products` unchanged.'],
        'products = [{"name": "Tea", "stock": 2}, {"name": "Cake", "stock": 5}, {"name": "Coffee", "stock": 1}]\ntarget = 5\n',
        'products = [{"name": "Tea", "stock": 2}, {"name": "Cake", "stock": 5}, {"name": "Coffee", "stock": 1}]\ntarget = 5\nrestock = [{"name": p["name"], "buy": target - p["stock"]} for p in products if p["stock"] < target]\nrestock = sorted(restock, key=lambda row: row["name"])',
        [('Calculate and sort the plan', 'assert restock == [{"name": "Coffee", "buy": 4}, {"name": "Tea", "buy": 3}]'), ('Preserve the original records', 'assert products == [{"name": "Tea", "stock": 2}, {"name": "Cake", "stock": 5}, {"name": "Coffee", "stock": 1}]')],
        ['Filter on stock < target.', 'Create new dictionaries instead of editing the product dictionaries.', 'Sort by the name field with a key function.'],
        'The plan separates current state from a proposed action. Cake is already at target, so it requires no restock entry.',
        ['A key function selects the value used for comparison.', 'sorted returns a new ordered list.', 'The dictionaries inside that list describe actions.'], 'Including products already at target adds zero-quantity actions that make a plan harder to review.', kind='checkpoint', minutes=18)

    # Remaining modules are expanded in a separate file to keep the material editable.
    from course_practice_more import add_practice
    add_practice(add)
    for m in modules:
        original = m['tasks']
        expanded = []
        for item in original:
            expanded.append(item)
            expanded.extend(insertions.pop((m['id'], item['id'][len(m['id']) + 1:]), []))
        m['tasks'] = expanded
    if insertions:
        raise ValueError(f'Practice anchors not found: {list(insertions)}')
    from course_reference import REFERENCES
    for m in modules:
        m['reference'] = REFERENCES[m['id']]
