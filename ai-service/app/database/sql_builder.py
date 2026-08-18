from app.services.search_filters import SearchFilters


class SQLBuilder:

    def build(
        self,
        filters: SearchFilters,
        include_branch: bool = True,
    ) -> str:

        # =====================================================
        # BASE CONDITIONS
        # =====================================================

        conditions = [
            "b.isactive = TRUE",
            "i.quantity > 0",
        ]

        # =====================================================
        # BRAND
        # =====================================================

        if filters.brand:

            brand = filters.brand.replace("'", "''")

            conditions.append(
                f"LOWER(p.productbrand) = LOWER('{brand}')"
            )

        # =====================================================
        # MODEL
        # =====================================================

        if filters.model:

            model = filters.model.replace("'", "''")

            conditions.append(
                f"LOWER(p.productmodel) = LOWER('{model}')"
            )

        # =====================================================
        # GENDER
        # =====================================================

        if filters.gender:

            gender_values = []

            for gender in filters.gender:

                escaped_gender = gender.replace(
                    "'",
                    "''",
                )

                gender_values.append(
                    f"LOWER('{escaped_gender}')"
                )

            genders_sql = ", ".join(
                gender_values
            )

            conditions.append(
                f"LOWER(p.productgender) IN ({genders_sql})"
            )

        # =====================================================
        # CATEGORY
        # =====================================================

        if filters.category:

            category = filters.category.replace(
                "'",
                "''",
            )

            conditions.append(
                f"LOWER(p.productcategory) = "
                f"LOWER('{category}')"
            )

        # =====================================================
        # USAGE
        # =====================================================

        if filters.usage:

            usage = filters.usage.replace(
                "'",
                "''",
            )

            conditions.append(
                f"LOWER(p.productusage) = "
                f"LOWER('{usage}')"
            )

        # =====================================================
        # SIZE
        # =====================================================

        if filters.size is not None:

            conditions.append(
                f"i.productsize = {int(filters.size)}"
            )

        # =====================================================
        # MAX PRICE
        # =====================================================

        if filters.max_price is not None:

            conditions.append(
                f"p.productprice <= "
                f"{float(filters.max_price)}"
            )

        # =====================================================
        # MIN PRICE
        # =====================================================

        if filters.min_price is not None:

            conditions.append(
                f"p.productprice >= "
                f"{float(filters.min_price)}"
            )

        # =====================================================
        # BRANCH
        # =====================================================

        if include_branch and filters.branch:

            branch = filters.branch.replace(
                "'",
                "''",
            )

            conditions.append(
                f"LOWER(b.branchname) = "
                f"LOWER('{branch}')"
            )

        # =====================================================
        # WHERE CLAUSE
        # =====================================================

        where_clause = "\n        AND ".join(
            conditions
        )

        # =====================================================
        # SQL QUERY
        # =====================================================

        return f"""
SELECT

    -- =====================================================
    -- BASIC PRODUCT INFORMATION
    -- =====================================================

    p.productid AS productid,
    p.productsku AS productsku,
    p.productname AS productname,
    p.productbrand AS productbrand,
    p.productmodel AS productmodel,
    p.productprice AS productprice,
    p.productgender AS productgender,
    p.productcategory AS productcategory,
    p.productusage AS productusage,

    -- =====================================================
    -- PRODUCT SPECIFICATIONS
    -- =====================================================

    p.productmaterial AS material,
    p.productsurface AS surface,
    p.productsupporttype AS supporttype,
    p.productcushioning AS cushioning,
    p.productbreathability AS breathability,
    p.productweight AS weight,
    p.productwaterproof AS waterproof,
    p.productdescription AS description,

    p.recommendeddistance AS recommendeddistance,
    p.archtype AS archtype,
    p.footstrike AS footstrike,
    p.energyreturn AS energyreturn,
    p.releaseyear AS releaseyear,
    p.heeldropmm AS heeldropmm,
    p.terrain AS terrain,

    -- =====================================================
    -- INVENTORY
    -- =====================================================

    i.productsize AS productsize,
    i.quantity AS quantity,

    -- =====================================================
    -- BRANCH
    -- =====================================================

    b.branchname AS branchname,
    b.city AS city

FROM products p

JOIN storeinventory i
    ON p.productid = i.productid

JOIN branches b
    ON i.branchid = b.branchid

WHERE {where_clause}

-- Most expensive first
ORDER BY p.productprice DESC

LIMIT 100;
""".strip()