from app.services.search_filters import SearchFilters


class SQLBuilder:

    def build(self, filters: SearchFilters, include_branch: bool = True) -> str:

        conditions = [
            "b.isactive = TRUE",
            "i.quantity > 0",
        ]

        if filters.gender:
            genders = ", ".join(
                f"'{gender}'"
                for gender in filters.gender
            )
            conditions.append(
                f"p.productgender IN ({genders})"
            )

        if filters.category:
            conditions.append(
                f"p.productcategory = '{filters.category}'"
            )

        if filters.usage:
            conditions.append(
                f"p.productusage = '{filters.usage}'"
            )

        if filters.size is not None:
            conditions.append(
                f"i.productsize = {filters.size}"
            )

        if filters.max_price is not None:
            conditions.append(
                f"p.productprice < {filters.max_price}"
            )

        if filters.min_price is not None:
            conditions.append(
                f"p.productprice >= {filters.min_price}"
            )

        if include_branch and filters.branch:
            conditions.append(
                f"b.branchname = '{filters.branch}'"
            )

        where_clause = "\n        AND ".join(conditions)

        return f"""
SELECT
    p.productid,
    p.productname,
    p.productbrand,
    p.productmodel,
    p.productprice,
    p.productgender,
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
WHERE {where_clause}
ORDER BY p.productprice
LIMIT 10;
""".strip()