from app.database.database import DatabaseService


def run(database, title, sql):
    print("=" * 60)
    print(title)
    print("=" * 60)

    try:
        results = database.execute_query(sql)

        for row in results:
            print(row)

        if not results:
            print("NO RESULTS")

    except Exception as exc:
        print("ERROR:", exc)

    print()


def main():

    database = DatabaseService()

    # ---------------------------------------------------------
    # TEST 1 — Long-distance products
    # ---------------------------------------------------------

    run(
        database,
        "1. LONG DISTANCE PRODUCTS",
        """
        SELECT
            productid,
            productname,
            productgender,
            productcategory,
            productusage,
            productprice
        FROM products
        WHERE productusage = 'Long Distance'
        ORDER BY productprice;
        """
    )

    # ---------------------------------------------------------
    # TEST 2 — Long distance + running
    # ---------------------------------------------------------

    run(
        database,
        "2. LONG DISTANCE + RUNNING",
        """
        SELECT
            productid,
            productname,
            productgender,
            productcategory,
            productusage,
            productprice
        FROM products
        WHERE productusage = 'Long Distance'
        AND productcategory = 'Running'
        ORDER BY productprice;
        """
    )

    # ---------------------------------------------------------
    # TEST 3 — Add gender + price
    # ---------------------------------------------------------

    run(
        database,
        "3. RUNNING + LONG DISTANCE + GENDER + PRICE",
        """
        SELECT
            productid,
            productname,
            productgender,
            productcategory,
            productusage,
            productprice
        FROM products
        WHERE productusage = 'Long Distance'
        AND productcategory = 'Running'
        AND productgender IN ('Men', 'Unisex')
        AND productprice < 7000
        ORDER BY productprice;
        """
    )

    # ---------------------------------------------------------
    # TEST 4 — Add inventory size
    # ---------------------------------------------------------

    run(
        database,
        "4. ADD SIZE 42",
        """
        SELECT
            p.productid,
            p.productname,
            p.productprice,
            p.productgender,
            p.productcategory,
            p.productusage,
            i.productsize,
            i.quantity
        FROM products p
        JOIN storeinventory i
            ON p.productid = i.productid
        WHERE p.productusage = 'Long Distance'
        AND p.productcategory = 'Running'
        AND p.productgender IN ('Men', 'Unisex')
        AND p.productprice < 7000
        AND i.productsize = 42
        ORDER BY p.productprice;
        """
    )

    # ---------------------------------------------------------
    # TEST 5 — Add stock
    # ---------------------------------------------------------

    run(
        database,
        "5. ADD AVAILABLE STOCK",
        """
        SELECT
            p.productid,
            p.productname,
            p.productprice,
            p.productgender,
            p.productcategory,
            p.productusage,
            i.productsize,
            i.quantity
        FROM products p
        JOIN storeinventory i
            ON p.productid = i.productid
        WHERE p.productusage = 'Long Distance'
        AND p.productcategory = 'Running'
        AND p.productgender IN ('Men', 'Unisex')
        AND p.productprice < 7000
        AND i.productsize = 42
        AND i.quantity > 0
        ORDER BY p.productprice;
        """
    )

    # ---------------------------------------------------------
    # TEST 6 — Add Nasr City
    # ---------------------------------------------------------

    run(
        database,
        "6. FINAL NASR CITY QUERY",
        """
        SELECT
            p.productid,
            p.productname,
            p.productbrand,
            p.productprice,
            p.productcategory,
            p.productusage,
            i.productsize,
            i.quantity,
            b.branchname,
            b.city
        FROM products p
        JOIN storeinventory i
            ON p.productid = i.productid
        JOIN branches b
            ON i.branchid = b.branchid
        WHERE b.isactive = TRUE
        AND i.quantity > 0
        AND i.productsize = 42
        AND p.productprice < 7000
        AND p.productgender IN ('Men', 'Unisex')
        AND p.productcategory = 'Running'
        AND p.productusage = 'Long Distance'
        AND b.branchname ILIKE '%Nasr City%'
        ORDER BY p.productprice;
        """
    )
    run(
    database,
    "7. SKECHERS SIZE 42 BY BRANCH",
    """
    SELECT
        p.productid,
        p.productname,
        p.productprice,
        i.productsize,
        i.quantity,
        i.branchid,
        b.branchname,
        b.city,
        b.address,
        b.isactive
    FROM products p
    JOIN storeinventory i
        ON p.productid = i.productid
    JOIN branches b
        ON i.branchid = b.branchid
    WHERE p.productid = 49
    AND i.productsize = 42
    ORDER BY i.branchid;
    """
)


if __name__ == "__main__":
    main()