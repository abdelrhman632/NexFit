from app.services.search_filters import SearchFilters
from app.database.sql_builder import SQLBuilder


def main():

    builder = SQLBuilder()

    filters = SearchFilters(
        gender=["Men", "Unisex"],
        category="Running",
        usage="Long Distance",
        size=42,
        max_price=7000,
        branch="Nasr City Branch",
    )

    print("=" * 60)
    print("PRIMARY QUERY")
    print("=" * 60)

    primary_sql = builder.build(filters)

    print(primary_sql)

    print()
    print("=" * 60)
    print("FALLBACK QUERY")
    print("=" * 60)

    fallback_sql = builder.build(
        filters,
        include_branch=False,
    )

    print(fallback_sql)


if __name__ == "__main__":
    main()