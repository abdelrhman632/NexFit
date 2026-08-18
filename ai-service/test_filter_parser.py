from app.services.filter_parser import FilterParser


def main():

    parser = FilterParser()

    # ---------------------------------------------------------
    # TEST 1
    # Gemini returns correct types
    # ---------------------------------------------------------

    data_1 = {
        "filters": {
            "gender": ["Men", "Unisex"],
            "category": "Running",
            "usage": "Long Distance",
            "size": 42,
            "max_price": 7000,
            "min_price": None,
            "branch": "Nasr City Branch",
        }
    }

    result = parser.parse(data_1)

    print("=" * 60)
    print("TEST 1: NORMAL TYPES")
    print("=" * 60)
    print(result)

    # ---------------------------------------------------------
    # TEST 2
    # Gemini returns numeric values as strings
    # ---------------------------------------------------------

    data_2 = {
        "filters": {
            "gender": "Men",
            "category": "Running",
            "usage": "Long Distance",
            "size": "42",
            "max_price": "7000",
            "min_price": None,
            "branch": "Nasr City Branch",
        }
    }

    result = parser.parse(data_2)

    print("=" * 60)
    print("TEST 2: STRING NUMBERS")
    print("=" * 60)
    print(result)

    # ---------------------------------------------------------
    # TEST 3
    # Missing optional filters
    # ---------------------------------------------------------

    data_3 = {
        "filters": {
            "category": "Running"
        }
    }

    result = parser.parse(data_3)

    print("=" * 60)
    print("TEST 3: PARTIAL FILTERS")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()