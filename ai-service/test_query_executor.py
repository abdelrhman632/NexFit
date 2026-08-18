from app.database.query_executor import QueryExecutor


def main():

    executor = QueryExecutor()

    safe_sql = """
    SELECT
        p.productid,
        p.productname,
        p.productbrand,
        p.productprice
    FROM products p
    WHERE p.productgender = 'Men'
    AND p.productcategory = 'Running'
    LIMIT 5;
    """

    dangerous_sql = """
    DELETE FROM products
    WHERE productid = 1;
    """

    print("=" * 60)
    print("TEST 1: SAFE QUERY")
    print("=" * 60)

    try:
        results = executor.execute(safe_sql)

        for row in results:
            print(row)

    except Exception as exc:
        print("ERROR:", exc)

    print()
    print("=" * 60)
    print("TEST 2: DANGEROUS QUERY")
    print("=" * 60)

    try:
        results = executor.execute(dangerous_sql)

        print("UNEXPECTED SUCCESS:")
        print(results)

    except Exception as exc:
        print("EXPECTED REJECTION:")
        print(exc)


if __name__ == "__main__":
    main()