DO $$
DECLARE
    b RECORD;
    p RECORD;
    shoe_size INT;
    product_limit INT;
    stock INT;

    colors TEXT[] := ARRAY[
        'Black',
        'White',
        'Blue',
        'Grey',
        'Red'
    ];
BEGIN

FOR b IN
SELECT BranchID
FROM Branches
LOOP

    IF b.BranchID <= 5 THEN
        product_limit := 200;

    ELSIF b.BranchID <= 12 THEN
        product_limit := 140;

    ELSE
        product_limit := 85;
    END IF;

    FOR p IN

        SELECT *
        FROM Products
        ORDER BY RANDOM()
        LIMIT product_limit

    LOOP

        FOR shoe_size IN 39..45 LOOP

            IF RANDOM() < 0.80 THEN

                stock := CASE

                    WHEN RANDOM() < 0.10 THEN 0

                    WHEN RANDOM() < 0.25 THEN FLOOR(RANDOM()*2)+1

                    WHEN RANDOM() < 0.75 THEN FLOOR(RANDOM()*6)+3

                    WHEN RANDOM() < 0.95 THEN FLOOR(RANDOM()*12)+9

                    ELSE FLOOR(RANDOM()*20)+21

                END;

                INSERT INTO StoreInventory
                (
                    BranchID,
                    ProductID,
                    ProductSize,
                    ProductColor,
                    Quantity
                )
                VALUES
                (
                    b.BranchID,
                    p.ProductID,
                    shoe_size,
                    colors[(FLOOR(RANDOM()*5)+1)::INT],
                    stock
                );

            END IF;

        END LOOP;

    END LOOP;

END LOOP;

END;
$$;