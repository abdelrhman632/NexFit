from app.database.database import DatabaseService


def run_test(database, title, sql):
    print("=" * 60)
    print(title)
    print("=" * 60)

    try:
        results = database.execute_query(sql)

        if not results:
            print("NO RESULTS")
        else:
            for row in results:
                print(row)

    except Exception as exc:
        print("ERROR:", exc)

    print()


def main():

    database = DatabaseService()

    # ---------------------------------------------------------
    # 1. Product genders
    # ---------------------------------------------------------

    run_test(
        database,
        "PRODUCT GENDERS",
        """
        SELECT DISTINCT productgender
        FROM products
        ORDER BY productgender;
        """
    )

    # ---------------------------------------------------------
    # 2. Product categories
    # ---------------------------------------------------------

    run_test(
        database,
        "PRODUCT CATEGORIES",
        """
        SELECT DISTINCT productcategory
        FROM products
        ORDER BY productcategory;
        """
    )

    # ---------------------------------------------------------
    # 3. Product usage
    # ---------------------------------------------------------

    run_test(
        database,
        "PRODUCT USAGE",
        """
        SELECT DISTINCT productusage
        FROM products
        ORDER BY productusage;
        """
    )

    # ---------------------------------------------------------
    # 4. Inventory sizes
    # ---------------------------------------------------------

    run_test(
        database,
        "INVENTORY SIZES",
        """
        SELECT DISTINCT productsize
        FROM storeinventory
        ORDER BY productsize;
        """
    )

    # ---------------------------------------------------------
    # 5. Branches
    # ---------------------------------------------------------

    run_test(
        database,
        "BRANCHES",
        """
        SELECT
            branchid,
            branchname,
            city,
            address,
            isactive
        FROM branches
        ORDER BY branchid;
        """
    )


if __name__ == "__main__":
    main()