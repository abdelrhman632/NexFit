DO $$
DECLARE
    p RECORD;
    b RECORD;
    shoe_size INT;
    product_limit INT;
    size_probability REAL;
    colors TEXT[] := ARRAY[
        'Black',
        'White',
        'Blue',
        'Grey',
        'Red'
    ];
BEGIN

FOR b IN SELECT BranchID FROM Branches LOOP

    -- Store tiers
    IF b.BranchID IN (1,2,3,4,5) THEN
        -- Flagship
        product_limit := 150;
        size_probability := 0.85;

    ELSIF b.BranchID IN (6,7,8,9,10,11,12,13,14,15) THEN
        -- Medium
        product_limit := 100;
        size_probability := 0.70;

    ELSE
        -- Small
        product_limit := 75;
        size_probability := 0.55;
    END IF;

    FOR p IN

        SELECT *
        FROM Products
        ORDER BY RANDOM()
        LIMIT product_limit

    LOOP

        FOR shoe_size IN 39..45 LOOP

            IF RANDOM() < size_probability THEN

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
                    colors[(floor(random()*5)+1)::INT],

                    CASE

                        -- Out of stock
                        WHEN RANDOM() < 0.10 THEN 0

                        -- 1 pair
                        WHEN RANDOM() < 0.45 THEN 1

                        -- 2 pairs
                        WHEN RANDOM() < 0.75 THEN 2

                        -- 3 pairs
                        WHEN RANDOM() < 0.90 THEN 3

                        -- 4 pairs
                        WHEN RANDOM() < 0.97 THEN 4

                        -- Rarely 5-6 pairs
                        ELSE floor(random()*2)+5

                    END
                );

            END IF;

        END LOOP;

    END LOOP;

END LOOP;

END $$;