DO $$
DECLARE
p RECORD;
b RECORD;
shoe_size INT;
product_limit INT;
colors TEXT[] := ARRAY[
'Black',
'White',
'Blue',
'Grey',
'Red'
];
BEGIN

FOR b IN
SELECT BranchID FROM Branches
LOOP

-- Large branches stock more products
IF b.BranchID IN (1,3,9,10,13) THEN
    product_limit := 50;
ELSE
    product_limit := 25;
END IF;

FOR p IN

SELECT *
FROM Products
WHERE

    ProductCategory IN ('Running','Walking','Lifestyle')

    OR

    (
        ProductCategory='Training'
        AND RANDOM() < 0.75
    )

    OR

    (
        ProductCategory='Football'
        AND b.BranchID IN (1,3,9,10,13)
    )

    OR

    (
        ProductCategory='Basketball'
        AND b.BranchID IN (1,3,9,10,13)
    )

    OR

    (
        ProductCategory='Tennis'
        AND b.BranchID IN (1,3,9,10,13)
    )

    OR

    (
        ProductCategory='Hiking'
        AND b.BranchID IN (3,9,10,13)
    )

    OR

    (
        ProductCategory='Trail Running'
        AND b.BranchID IN (3,9,10,13)
    )

ORDER BY RANDOM()

LIMIT product_limit

LOOP

    FOR shoe_size IN 39..45 LOOP

        IF RANDOM() < 0.80 THEN

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

                CASE

                    WHEN RANDOM() < 0.05 THEN 0

                    WHEN RANDOM() < 0.20 THEN 1

                    ELSE FLOOR(RANDOM()*10)+2

                END
            );

        END IF;

    END LOOP;

END LOOP;


END LOOP;

END $$;