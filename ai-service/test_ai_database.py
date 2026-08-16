import json

from app.services.llm import LLMService
from app.services.filter_parser import FilterParser
from app.services.filter_validator import FilterValidator, FilterValidationError
from app.database.sql_builder import SQLBuilder
from app.database.query_executor import QueryExecutor


def parse_gemini_json(response_text: str) -> dict:
    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return json.loads(text)


def main():

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
    # STEP 1 — Gemini
    # =========================================================

    llm = LLMService()

    print("=" * 60)
    print("GENERATING FILTERS WITH GEMINI")
    print("=" * 60)

    response = llm.generate_sql(user_text)

    print(response)

    # =========================================================
    # STEP 2 — Parse Gemini JSON
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
    # STEP 3 — Check whether database is needed
    # =========================================================

    needs_database = data.get("needs_database", False)

    if not needs_database:
        print("=" * 60)
        print("DATABASE NOT REQUIRED")
        print("=" * 60)
        return

    # =========================================================
    # STEP 4 — JSON → SearchFilters
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
    # STEP 5 — Validate filters
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
    # STEP 6 — Build SQL
    # =========================================================

    print("=" * 60)
    print("BUILDING SQL")
    print("=" * 60)

    builder = SQLBuilder()

    sql = builder.build(filters)

    print(sql)

    # =========================================================
    # STEP 7 — Execute through QueryExecutor
    # =========================================================

    print("=" * 60)
    print("EXECUTING DATABASE QUERY")
    print("=" * 60)

    executor = QueryExecutor()

    try:
        results = executor.execute(sql)

    except Exception as exc:
        print("DATABASE ERROR:")
        print(exc)
        return

    # =========================================================
    # STEP 8 — Results
    # =========================================================

    print("=" * 60)
    print("DATABASE RESULTS")
    print("=" * 60)

    if not results:
        print("No matching products found.")
        return

    print(f"Found {len(results)} result(s).")

    for index, row in enumerate(results, start=1):
        print()
        print(f"RESULT {index}")
        print(row)


if __name__ == "__main__":
    main()