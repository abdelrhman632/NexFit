from app.services.search_filters import SearchFilters
from app.services.filter_validator import (
    FilterValidator,
    FilterValidationError,
)


def test(name, filters):

    print("=" * 60)
    print(name)
    print("=" * 60)

    try:
        validated = FilterValidator().validate(filters)

        print("VALID: True")
        print("FILTERS:")
        print(validated)

    except FilterValidationError as exc:

        print("VALID: False")
        print("ERROR:", exc)

    print()


def main():

    # ---------------------------------------------------------
    # TEST 1 — Valid filters
    # ---------------------------------------------------------

    test(
        "TEST 1: VALID FILTERS",
        SearchFilters(
            gender=["Men", "Unisex"],
            category="Running",
            usage="Long Distance",
            size=42,
            max_price=7000,
            branch="Nasr City Branch",
        ),
    )

    # ---------------------------------------------------------
    # TEST 2 — Invalid category
    # ---------------------------------------------------------

    test(
        "TEST 2: INVALID CATEGORY",
        SearchFilters(
            gender=["Men"],
            category="Swimming",
        ),
    )

    # ---------------------------------------------------------
    # TEST 3 — Invalid size
    # ---------------------------------------------------------

    test(
        "TEST 3: INVALID SIZE",
        SearchFilters(
            size=50,
        ),
    )

    # ---------------------------------------------------------
    # TEST 4 — Invalid branch
    # ---------------------------------------------------------

    test(
        "TEST 4: INVALID BRANCH",
        SearchFilters(
            branch="Jeddah Branch",
        ),
    )

    # ---------------------------------------------------------
    # TEST 5 — No optional filters
    # ---------------------------------------------------------

    test(
        "TEST 5: EMPTY FILTERS",
        SearchFilters(),
    )


if __name__ == "__main__":
    main()