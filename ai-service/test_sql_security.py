from app.database.sql_validator import validate_sql


def test_sql(name: str, sql: str):

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

    # =========================================================
    # TEST 1 — SAFE SELECT
    # =========================================================

    safe_sql = """
    SELECT
        p.productid,
        p.productname,
        p.productprice
    FROM products p
    WHERE p.productprice < 7000;
    """

    # =========================================================
    # TEST 2 — DANGEROUS DELETE
    # =========================================================

    delete_sql = """
    DELETE FROM products
    WHERE productprice < 7000;
    """

    # =========================================================
    # TEST 3 — DANGEROUS UPDATE
    # =========================================================

    update_sql = """
    UPDATE products
    SET productprice = 1
    WHERE productid = 1;
    """

    # =========================================================
    # TEST 4 — DANGEROUS DROP
    # =========================================================

    drop_sql = """
    DROP TABLE products;
    """

    # =========================================================
    # TEST 5 — DANGEROUS INSERT
    # =========================================================

    insert_sql = """
    INSERT INTO products
    (productname, productprice)
    VALUES
    ('Hacked Shoe', 1);
    """

    # =========================================================
    # RUN TESTS
    # =========================================================

    test_sql(
        "TEST 1: SAFE SELECT",
        safe_sql,
    )

    test_sql(
        "TEST 2: DANGEROUS DELETE",
        delete_sql,
    )

    test_sql(
        "TEST 3: DANGEROUS UPDATE",
        update_sql,
    )

    test_sql(
        "TEST 4: DANGEROUS DROP",
        drop_sql,
    )

    test_sql(
        "TEST 5: DANGEROUS INSERT",
        insert_sql,
    )


if __name__ == "__main__":
    main()