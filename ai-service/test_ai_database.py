import json

from app.services.llm import LLMService
from app.services.filter_parser import FilterParser
from app.services.filter_validator import (
    FilterValidator,
    FilterValidationError,
)
from app.database.sql_builder import SQLBuilder
from app.database.query_executor import QueryExecutor


def parse_gemini_json(response_text: str) -> dict:
    """
    Convert Gemini's JSON response into a Python dictionary.

    Handles accidental Markdown code fences such as:
    ```json
    {...}
    ```
    """

    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)


def print_results(title: str, results: list):

    print("=" * 60)
    print(title)
    print("=" * 60)

    if not results:
        print("No matching products found.")
        return

    print(f"Found {len(results)} result(s).")

    for index, row in enumerate(results, start=1):

        print()
        print(f"RESULT {index}")

        for key, value in row.items():
            print(f"{key}: {value}")


def main():

    # =========================================================
    # USER REQUEST
    # =========================================================

    user_text = """
    انا محتاج جزمه رجالي للجري لمسافات طويله
    مقاس 42
    اقل من 7000 جنيه
    وتكون موجوده في مدينه نصر.
    """

    print("=" * 60)
    print("USER REQUEST")
    print("=" * 60)
    print(user_text)

    # =========================================================
    # STEP 1 — GEMINI
    # =========================================================

    print("=" * 60)
    print("GENERATING FILTERS WITH GEMINI")
    print("=" * 60)

    llm = LLMService()

    try:
        response = llm.generate_sql(user_text)

    except Exception as exc:
        print("GEMINI ERROR:")
        print(exc)
        return

    print(response)

    # =========================================================
    # STEP 2 — PARSE GEMINI JSON
    # =========================================================

    try:
        data = parse_gemini_json(response)

    except json.JSONDecodeError as exc:
        print("=" * 60)
        print("INVALID GEMINI JSON")
        print("=" * 60)
        print(exc)
        return

    # =========================================================
    # STEP 3 — CHECK DATABASE REQUIREMENT
    # =========================================================

    needs_database = data.get("needs_database", False)

    if not needs_database:

        print("=" * 60)
        print("DATABASE NOT REQUIRED")
        print("=" * 60)

        reason = data.get("reason")

        if reason:
            print("REASON:")
            print(reason)

        return

    # Gemini must provide filters when database access is required.

    if not data.get("filters"):

        print("=" * 60)
        print("ERROR: GEMINI RETURNED NO FILTERS")
        print("=" * 60)

        return

    # =========================================================
    # STEP 4 — JSON → SEARCH FILTERS
    # =========================================================

    print("=" * 60)
    print("PARSING SEARCH FILTERS")
    print("=" * 60)

    try:

        filters = FilterParser().parse(data)

        print(filters)

    except ValueError as exc:

        print("FILTER PARSING ERROR:")
        print(exc)

        return

    # =========================================================
    # STEP 5 — VALIDATE FILTERS
    # =========================================================

    print("=" * 60)
    print("VALIDATING FILTERS")
    print("=" * 60)

    try:

        filters = FilterValidator().validate(filters)

        print("FILTERS VALID")
        print(filters)

    except FilterValidationError as exc:

        print("FILTER VALIDATION FAILED:")
        print(exc)

        return

    # =========================================================
    # STEP 6 — BUILD PRIMARY SQL
    # =========================================================

    print("=" * 60)
    print("BUILDING PRIMARY SQL")
    print("=" * 60)

    builder = SQLBuilder()

    sql = builder.build(
        filters,
        include_branch=True,
    )

    print(sql)

    # =========================================================
    # STEP 7 — EXECUTE PRIMARY QUERY
    # =========================================================

    print("=" * 60)
    print("EXECUTING PRIMARY DATABASE QUERY")
    print("=" * 60)

    executor = QueryExecutor()

    try:

        results = executor.execute(sql)

    except Exception as exc:

        print("DATABASE ERROR:")
        print(exc)

        return

    # =========================================================
    # STEP 8 — PRIMARY RESULTS
    # =========================================================

    print_results(
        "PRIMARY DATABASE RESULTS",
        results,
    )

    # =========================================================
    # STEP 9 — LOCATION FALLBACK
    # =========================================================

    if results:

        print()
        print("Exact matches found.")
        return

    # No exact results.

    if not filters.branch:

        print()
        print("No branch was requested.")
        print("No location fallback is required.")

        return

    print()
    print("=" * 60)
    print("NO EXACT MATCHES")
    print("=" * 60)

    print(
        f"No products matched all requirements at: "
        f"{filters.branch}"
    )

    print()
    print("=" * 60)
    print("TRYING WITHOUT BRANCH FILTER")
    print("=" * 60)

    fallback_sql = builder.build(
        filters,
        include_branch=False,
    )

    print(fallback_sql)

    # =========================================================
    # STEP 10 — EXECUTE FALLBACK QUERY
    # =========================================================

    print("=" * 60)
    print("EXECUTING FALLBACK DATABASE QUERY")
    print("=" * 60)

    try:

        fallback_results = executor.execute(
            fallback_sql
        )

    except Exception as exc:

        print("FALLBACK DATABASE ERROR:")
        print(exc)

        return

    # =========================================================
    # STEP 11 — FALLBACK RESULTS
    # =========================================================

    print_results(
        "FALLBACK RESULTS",
        fallback_results,
    )

    # =========================================================
    # STEP 12 — FINAL STATUS
    # =========================================================

    print()
    print("=" * 60)
    print("FINAL STATUS")
    print("=" * 60)

    if fallback_results:

        print(
            "Products matching the requested criteria "
            "were found at other branches."
        )

    else:

        print(
            "No products matching the requested criteria "
            "were found anywhere."
        )


if __name__ == "__main__":
    main()