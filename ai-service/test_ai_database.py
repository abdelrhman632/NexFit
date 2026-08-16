import json

from app.services.llm import LLMService
from app.database.query_executor import QueryExecutor


def parse_gemini_json(response_text: str) -> dict:
    """
    Parse Gemini's JSON response.

    Handles both:
    1. Raw JSON
    2. JSON wrapped in ```json ... ```
    """

    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        # Remove opening ```json / ```
        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        # Remove closing ```
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

    # ---------------------------------------------------------
    # STEP 1 — Gemini generates SQL
    # ---------------------------------------------------------

    llm = LLMService()

    print()
    print("=" * 60)
    print("GENERATING SQL WITH GEMINI")
    print("=" * 60)

    llm_response = llm.generate_sql(user_text)

    print(llm_response)

    # ---------------------------------------------------------
    # STEP 2 — Parse Gemini response
    # ---------------------------------------------------------

    try:
        data = parse_gemini_json(llm_response)

    except json.JSONDecodeError as exc:
        print()
        print("=" * 60)
        print("ERROR: INVALID GEMINI JSON")
        print("=" * 60)
        print(exc)
        return

    needs_database = data.get("needs_database", False)
    sql = data.get("sql")

    print()
    print("=" * 60)
    print("PARSED GEMINI RESPONSE")
    print("=" * 60)

    print("Needs database:", needs_database)
    print("SQL:")
    print(sql)

    # ---------------------------------------------------------
    # STEP 3 — No database needed
    # ---------------------------------------------------------

    if not needs_database:
        print()
        print("Gemini determined that no database query is required.")
        return

    # ---------------------------------------------------------
    # STEP 4 — Validate SQL exists
    # ---------------------------------------------------------

    if not sql:
        print()
        print("ERROR: Database was required but Gemini returned no SQL.")
        return

    # ---------------------------------------------------------
    # STEP 5 — Validate + execute
    # ---------------------------------------------------------

    executor = QueryExecutor()

    print()
    print("=" * 60)
    print("VALIDATING AND EXECUTING SQL")
    print("=" * 60)

    try:
        results = executor.execute(sql)

    except Exception as exc:
        print()
        print("=" * 60)
        print("QUERY REJECTED / DATABASE ERROR")
        print("=" * 60)
        print(exc)
        return

    # ---------------------------------------------------------
    # STEP 6 — Print results
    # ---------------------------------------------------------

    print()
    print("=" * 60)
    print("DATABASE RESULTS")
    print("=" * 60)

    if not results:
        print("No matching products found.")
        return

    print(f"Found {len(results)} result(s).")
    print()

    for index, row in enumerate(results, start=1):
        print(f"RESULT {index}")
        print(row)
        print()


if __name__ == "__main__":
    main()