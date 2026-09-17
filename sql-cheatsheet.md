# SQL Transformation Cheatsheet

A general reference for learning SQL transformations, aggregation, dates, subqueries, CTEs, and window functions.

---

# 1. Basic SELECT

```sql
SELECT column_1, column_2
FROM table_name;
```

Select all columns:

```sql
SELECT *
FROM table_name;
```

Rename a column:

```sql
SELECT
    column_name AS new_name
FROM table_name;
```

---

# 2. Filtering with WHERE

```sql
SELECT *
FROM table_name
WHERE numeric_column > 10;
```

Multiple conditions:

```sql
WHERE condition_1
  AND condition_2
```

```sql
WHERE condition_1
   OR condition_2
```

Useful operators:

```sql
=       -- equal
!=      -- not equal
>       -- greater than
>=      -- greater than or equal
<       -- less than
<=      -- less than or equal
```

Other useful filters:

```sql
BETWEEN
IN
LIKE
IS NULL
IS NOT NULL
```

Examples:

```sql
WHERE numeric_column BETWEEN 10 AND 20
```

```sql
WHERE category_column IN ('A', 'B', 'C')
```

```sql
WHERE text_column LIKE 'abc%'
```

---

# 3. Sorting

Ascending:

```sql
ORDER BY column_name ASC;
```

Descending:

```sql
ORDER BY column_name DESC;
```

Multiple sort rules:

```sql
ORDER BY
    column_1 ASC,
    column_2 DESC;
```

---

# 4. LIMIT

Return only a certain number of rows:

```sql
SELECT *
FROM table_name
LIMIT 10;
```

Useful when inspecting data while developing a query.

---

# 5. DISTINCT

Return unique values:

```sql
SELECT DISTINCT column_name
FROM table_name;
```

Unique combinations:

```sql
SELECT DISTINCT column_1, column_2
FROM table_name;
```

---

# 6. JOIN

Use joins to combine related tables.

Basic pattern:

```sql
SELECT
    a.column_1,
    b.column_2
FROM table_a AS a
JOIN table_b AS b
    ON a.key_column = b.key_column;
```

Common aliases:

```sql
table_name AS t
```

Aliases make larger queries easier to read.

---

# 7. Types of JOIN

## INNER JOIN

Only rows that match in both tables:

```sql
SELECT ...
FROM table_a AS a
INNER JOIN table_b AS b
    ON a.id = b.id;
```

`JOIN` by itself usually means `INNER JOIN`.

---

## LEFT JOIN

Keep every row from the left table:

```sql
SELECT ...
FROM table_a AS a
LEFT JOIN table_b AS b
    ON a.id = b.id;
```

If there is no matching row in `table_b`, its columns become `NULL`.

---

# 8. Aggregate Functions

Aggregate functions summarize multiple rows.

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
```

Examples:

```sql
SELECT COUNT(*)
FROM table_name;
```

```sql
SELECT AVG(numeric_column)
FROM table_name;
```

```sql
SELECT
    MIN(numeric_column),
    MAX(numeric_column)
FROM table_name;
```

---

# 9. GROUP BY

Use `GROUP BY` when you want one result per group.

General pattern:

```sql
SELECT
    grouping_column,
    AVG(numeric_column)
FROM table_name
GROUP BY grouping_column;
```

Grouping by several columns:

```sql
GROUP BY column_1, column_2
```

A useful mental question:

> What should one row in the output represent?

If you group by:

```sql
GROUP BY customer_id, year
```

then one result row represents:

```text
one customer + one year
```

---

# 10. Multiple Aggregations

You can calculate several summaries at once:

```sql
SELECT
    grouping_column,
    AVG(value) AS avg_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value,
    COUNT(*) AS row_count
FROM table_name
GROUP BY grouping_column;
```

---

# 11. WHERE vs HAVING

`WHERE` filters individual rows before aggregation.

```sql
WHERE value > 10
```

`HAVING` filters aggregated groups.

```sql
SELECT
    category,
    AVG(value) AS avg_value
FROM table_name
GROUP BY category
HAVING AVG(value) > 10;
```

Mental model:

```text
WHERE
↓
filter raw rows

GROUP BY
↓
aggregate

HAVING
↓
filter aggregated groups
```

---

# 12. CASE WHEN

Use `CASE` to create conditional transformations.

```sql
CASE
    WHEN condition_1 THEN result_1
    WHEN condition_2 THEN result_2
    ELSE result_3
END
```

Example structure:

```sql
SELECT
    CASE
        WHEN value >= threshold_1 THEN 'High'
        WHEN value >= threshold_2 THEN 'Medium'
        ELSE 'Low'
    END AS category
FROM table_name;
```

Multiple conditions:

```sql
CASE
    WHEN condition_1 AND condition_2 THEN result
    ELSE other_result
END
```

Useful for:

* categories
* flags
* scores
* business rules
* cleaning values

---

# 13. NULL

`NULL` means a value is missing or unknown.

Check for it with:

```sql
IS NULL
```

or:

```sql
IS NOT NULL
```

Do not use:

```sql
column = NULL
```

---

# 14. COALESCE

Return the first non-NULL value:

```sql
COALESCE(column_name, fallback_value)
```

Example:

```sql
COALESCE(value, 0)
```

Be careful:

Replacing missing data with `0` is only correct when zero actually has the intended meaning.

---

# 15. Arithmetic

You can calculate new columns directly:

```sql
SELECT
    column_1 + column_2 AS total
FROM table_name;
```

Operators:

```sql
+
-
*
/
```

Example structure:

```sql
SELECT
    revenue - cost AS profit
FROM table_name;
```

---

# 16. ROUND

Round numeric results:

```sql
ROUND(value, 2)
```

Example:

```sql
ROUND(AVG(value), 2)
```

---

# 17. CAST

Convert data from one type to another:

```sql
CAST(value AS INTEGER)
```

```sql
CAST(value AS REAL)
```

```sql
CAST(value AS TEXT)
```

Useful when extracted or imported data has the wrong type.

---

# 18. String Concatenation in SQLite

SQLite uses:

```sql
||
```

Example:

```sql
first_name || ' ' || last_name
```

Result:

```text
John Smith
```

---

# 19. SQLite Date and Time Functions

Important SQLite functions:

```sql
date()
time()
datetime()
julianday()
strftime()
```

---

# 20. Current Date and Time

Current date:

```sql
date('now')
```

Current date and time:

```sql
datetime('now')
```

---

# 21. Date Arithmetic

One day later:

```sql
date('now', '+1 day')
```

Seven days earlier:

```sql
date('now', '-7 days')
```

One month later:

```sql
date('now', '+1 month')
```

---

# 22. Creating a Datetime

If date and time are stored separately, they can be combined conceptually with:

```sql
date_column || ' ' || time_column
```

Then converted:

```sql
datetime(...)
```

General pattern:

```sql
datetime(date_column || ' ' || time_column)
```

---

# 23. julianday()

`julianday()` converts a datetime into a numeric representation.

This makes subtraction possible:

```sql
julianday(timestamp_2) - julianday(timestamp_1)
```

The result is measured in days.

Hours:

```sql
(
    julianday(timestamp_2)
    -
    julianday(timestamp_1)
) * 24
```

Minutes:

```sql
(
    julianday(timestamp_2)
    -
    julianday(timestamp_1)
) * 24 * 60
```

---

# 24. strftime()

Extract parts of a date or timestamp.

Year:

```sql
strftime('%Y', timestamp)
```

Month:

```sql
strftime('%m', timestamp)
```

Day:

```sql
strftime('%d', timestamp)
```

Hour:

```sql
strftime('%H', timestamp)
```

Minute:

```sql
strftime('%M', timestamp)
```

Day of week:

```sql
strftime('%w', timestamp)
```

Sometimes the result should be converted:

```sql
CAST(strftime('%H', timestamp) AS INTEGER)
```

---

# 25. Subqueries

A query can be used as the input to another query.

```sql
SELECT *
FROM (
    SELECT
        ...
    FROM table_name
);
```

Mental model:

```text
raw table
   ↓
inner query
   ↓
temporary result
   ↓
outer query
```

---

# 26. CTEs — WITH

A Common Table Expression gives a temporary query result a name.

```sql
WITH transformed AS (

    SELECT
        ...
    FROM table_name

)

SELECT *
FROM transformed;
```

This is often easier to read than a deeply nested subquery.

---

# 27. Multiple CTEs

```sql
WITH step_1 AS (

    SELECT ...
    FROM ...

),

step_2 AS (

    SELECT ...
    FROM step_1

),

step_3 AS (

    SELECT ...
    FROM step_2

)

SELECT *
FROM step_3;
```

This is extremely useful for building transformation pipelines.

Mental model:

```text
raw
 ↓
clean
 ↓
enrich
 ↓
aggregate
 ↓
rank / score
 ↓
output
```

---

# 28. MAX and MIN Per Group

A very common pattern:

```sql
SELECT
    grouping_column,
    MAX(value_column)
FROM table_name
GROUP BY grouping_column;
```

Conceptually:

```text
Group A → maximum value
Group B → maximum value
Group C → maximum value
```

The same works with:

```sql
MIN()
```

---

# 29. Aggregate Then Join Back

Sometimes you first find a value per group and then need the original row associated with it.

General structure:

```sql
WITH grouped AS (

    SELECT
        grouping_column,
        MAX(value_column) AS max_value
    FROM table_name
    GROUP BY grouping_column

)

SELECT ...
FROM table_name AS t
JOIN grouped AS g
    ON ...
```

This is a reusable SQL pattern worth recognizing.

---

# 30. Window Functions

Window functions calculate across related rows without collapsing them.

General syntax:

```sql
FUNCTION() OVER (
    PARTITION BY column
    ORDER BY column
)
```

Important window functions:

```sql
ROW_NUMBER()
RANK()
DENSE_RANK()
LAG()
LEAD()
```

Aggregate functions can also be windows:

```sql
AVG()
SUM()
MIN()
MAX()
```

---

# 31. GROUP BY vs Window Functions

`GROUP BY` collapses rows:

```text
many rows
   ↓
one row per group
```

Window functions keep the original rows:

```text
many rows
   ↓
same rows
+
extra calculated column
```

This distinction is fundamental.

---

# 32. PARTITION BY

`PARTITION BY` divides rows into groups for a window function.

```sql
FUNCTION() OVER (
    PARTITION BY category
)
```

Think:

> Perform the calculation separately inside each category.

Without `PARTITION BY`:

```text
all rows belong to one window
```

With it:

```text
group A → separate window
group B → separate window
group C → separate window
```

---

# 33. ROW_NUMBER

Assign a unique sequential number to rows:

```sql
ROW_NUMBER() OVER (
    ORDER BY sort_column
)
```

Restart numbering per group:

```sql
ROW_NUMBER() OVER (
    PARTITION BY grouping_column
    ORDER BY sort_column
)
```

General result:

```text
row | value | row_number
----|-------|-----------
... | ...   | 1
... | ...   | 2
... | ...   | 3
```

Useful for problems involving:

* first row
* latest row
* earliest row
* top N rows per group

---

# 34. RANK

Rank rows according to a value:

```sql
RANK() OVER (
    ORDER BY numeric_column DESC
)
```

Possible result:

```text
value | rank
------|-----
100   | 1
90    | 2
90    | 2
80    | 4
```

Notice the skipped rank after a tie.

---

# 35. DENSE_RANK

Similar to `RANK`, but does not skip numbers.

```text
value | dense_rank
------|-----------
100   | 1
90    | 2
90    | 2
80    | 3
```

Syntax:

```sql
DENSE_RANK() OVER (
    ORDER BY numeric_column DESC
)
```

---

# 36. LAG

Access the previous row's value:

```sql
LAG(value_column) OVER (
    ORDER BY ordering_column
)
```

Common pattern:

```sql
value_column
-
LAG(value_column) OVER (...)
```

Useful for:

* change from previous row
* growth
* differences over time
* previous observations

---

# 37. LEAD

Access the next row's value:

```sql
LEAD(value_column) OVER (
    ORDER BY ordering_column
)
```

Think:

```text
LAG  → previous row
LEAD → next row
```

---

# 38. Running Totals

Windowed `SUM`:

```sql
SUM(value_column) OVER (
    ORDER BY ordering_column
)
```

Conceptually:

```text
value | running total
------|--------------
10    | 10
20    | 30
5     | 35
```

---

# 39. Moving Averages

Example structure:

```sql
AVG(value_column) OVER (
    ORDER BY ordering_column
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

Meaning:

```text
current row
+
previous 2 rows
```

Useful for smoothing time-series data.

---

# 40. Conditional Aggregation

You can combine aggregates with `CASE`.

General structure:

```sql
SUM(
    CASE
        WHEN condition THEN 1
        ELSE 0
    END
)
```

This can count how many rows satisfy a condition.

Another pattern:

```sql
AVG(
    CASE
        WHEN condition THEN value
    END
)
```

Useful when aggregating subsets of data.

---

# 41. Percentages

General pattern:

```sql
part * 100.0 / total
```

Using `100.0` instead of `100` can help ensure decimal arithmetic.

Example structure:

```sql
COUNT(...) * 100.0 / COUNT(...)
```

---

# 42. Normalization

A common min-max normalization formula is:

```text
(value - minimum)
-----------------
(maximum - minimum)
```

SQL structure:

```sql
(value - min_value) * 1.0
/
(max_value - min_value)
```

Result is usually between:

```text
0 and 1
```

when the minimum and maximum are fixed appropriately.

---

# 43. Weighted Scores

General idea:

```text
score =
    metric_1 × weight_1
  + metric_2 × weight_2
  + metric_3 × weight_3
```

SQL pattern:

```sql
metric_1 * weight_1
+
metric_2 * weight_2
+
metric_3 * weight_3
```

This can also be combined with `CASE`.

```sql
CASE
    WHEN condition THEN points
    ELSE other_points
END
```

---

# 44. Bounding a Value in SQLite

SQLite scalar `MIN` and `MAX` can be used to restrict a calculation.

Lower boundary:

```sql
MAX(value, lower_bound)
```

Upper boundary:

```sql
MIN(value, upper_bound)
```

Both:

```sql
MAX(
    lower_bound,
    MIN(upper_bound, value)
)
```

Conceptually:

```text
value too low  → lower boundary
value valid    → value
value too high → upper boundary
```

---

# 45. CREATE VIEW

Save a query as a reusable virtual table:

```sql
CREATE VIEW view_name AS

SELECT
    ...
FROM ...;
```

Then query it:

```sql
SELECT *
FROM view_name;
```

Delete:

```sql
DROP VIEW IF EXISTS view_name;
```

A view stores the query logic rather than a separate copy of the data.

---

# 46. CREATE TABLE AS SELECT

Create a physical table from query results:

```sql
CREATE TABLE new_table AS

SELECT
    ...
FROM old_table;
```

Conceptual difference:

```text
VIEW
→ saved query

TABLE
→ saved rows
```

---

# 47. SQL Query Structure

Typical written order:

```sql
SELECT
FROM
JOIN
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

Template:

```sql
SELECT
    ...
FROM table_name AS t
JOIN other_table AS o
    ON ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...;
```

---

# 48. Logical Execution Order

SQL roughly evaluates clauses in this order:

```text
FROM
 ↓
JOIN
 ↓
WHERE
 ↓
GROUP BY
 ↓
HAVING
 ↓
SELECT
 ↓
ORDER BY
 ↓
LIMIT
```

This explains why aliases created in `SELECT` often cannot be used in earlier clauses such as `WHERE`.

---

# 49. Debugging Queries

Build complicated queries incrementally.

Start:

```sql
SELECT *
FROM table_name
LIMIT 10;
```

Then add one piece at a time:

```text
1. FROM
2. JOIN
3. selected columns
4. calculated columns
5. WHERE
6. GROUP BY
7. window functions
8. ORDER BY
```

After every major step, inspect the result.

This is much easier than debugging a large query all at once.

---

# 50. Questions to Ask Yourself

Before writing a transformation, ask:

### What should one output row represent?

Examples:

```text
one customer
one customer per month
one product per day
one transaction
```

### Am I reducing rows?

If yes, you may need:

```sql
GROUP BY
```

### Do I want to keep the rows but add information?

You may need:

```sql
window functions
```

### Do I need information from another table?

You may need:

```sql
JOIN
```

### Am I classifying values?

You may need:

```sql
CASE
```

### Am I comparing rows over time?

You may need:

```sql
LAG()
LEAD()
```

### Do I need the first/latest/top row inside each group?

Think about:

```sql
ROW_NUMBER()
PARTITION BY
ORDER BY
```

### Is the query becoming difficult to understand?

Break it into:

```sql
WITH step_1 AS (...),
step_2 AS (...),
step_3 AS (...)
```

---

# 51. Core SQL to Know Well

Focus especially on:

```sql
SELECT
FROM
WHERE
JOIN
GROUP BY
HAVING
ORDER BY
```

Aggregates:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
```

Transformations:

```sql
CASE
COALESCE()
CAST()
ROUND()
```

CTEs:

```sql
WITH ... AS (...)
```

SQLite dates:

```sql
date()
datetime()
julianday()
strftime()
```

Window functions:

```sql
ROW_NUMBER()
RANK()
DENSE_RANK()
LAG()
LEAD()
```

Window syntax:

```sql
OVER()
PARTITION BY
ORDER BY
```

If these become comfortable, you can solve a large share of practical SQL transformation problems without needing to memorize much else.
