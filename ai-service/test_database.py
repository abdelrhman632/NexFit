from app.database.database import DatabaseService


def main():

    database = DatabaseService()

    sql = """
    SELECT
        productid,
        productname,
        productprice
    FROM products
    LIMIT 5;
    """

    print("=" * 60)
    print("DATABASE TEST")
    print("=" * 60)

    try:
        results = database.execute_query(sql)

        print("Query executed successfully.")
        print()

        for row in results:
            print(row)

    except Exception as exc:
        print("DATABASE ERROR:")
        print(exc)


if __name__ == "__main__":
    main()