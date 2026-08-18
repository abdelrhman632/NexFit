from app.database.sql_validator import validate_sql


gemini_query = """
SELECT
    p.productid,
    p.productname,
    p.productbrand,
    p.productprice,
    s.productsize,
    s.quantity,
    b.branchname
FROM products p
JOIN storeinventory s
    ON p.productid = s.productid
JOIN branches b
    ON s.branchid = b.branchid
WHERE p.productgender = 'Men'
AND p.productcategory = 'Running'
AND p.productusage = 'Long Distance'
AND p.productprice < 7000
AND s.productsize = '42'
AND s.quantity > 0
AND b.isactive = TRUE
AND (
    b.branchname LIKE '%مدينة نصر%'
    OR b.city LIKE '%مدينة نصر%'
);
"""


def test_query(name: str, sql: str):
    valid, message = validate_sql(sql)

    print("=" * 60)
    print(name)
    print("=" * 60)
    print("SQL:")
    print(sql)
    print()
    print("VALID:", valid)
    print("MESSAGE:", message)
    print()


def main():

    safe_query = """
SELECT
    p.productid,
    p.productname,
    p.productprice
FROM products p
WHERE p.productgender = 'Men'
AND p.productcategory = 'Running';
"""

    dangerous_query = """
DELETE FROM products
WHERE productid = 1;
"""

    forbidden_table = """
SELECT
    password
FROM users;
"""

    forbidden_column = """
SELECT
    p.fake_column
FROM products p;
"""

    test_query("TEST 1: SAFE SELECT", safe_query)

    test_query("TEST 2: DANGEROUS DELETE", dangerous_query)

    test_query("TEST 3: FORBIDDEN TABLE", forbidden_table)

    test_query("TEST 4: FORBIDDEN COLUMN", forbidden_column)

    test_query("TEST 5: REAL GEMINI QUERY", gemini_query)


if __name__ == "__main__":
    main()