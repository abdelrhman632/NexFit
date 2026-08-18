from itertools import product
import json

from app.services.llm import LLMService
from app.services.product_search import ProductSearchService


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

    response = llm.generate_sql(user_text)

    print(response)

    # =========================================================
    # STEP 2 — PARSE GEMINI JSON
    # =========================================================

    data = parse_gemini_json(response)

    print("=" * 60)
    print("PARSED GEMINI DATA")
    print("=" * 60)
    print(data)

    # =========================================================
    # STEP 3 — PRODUCT SEARCH SERVICE
    # =========================================================

    print("=" * 60)
    print("RUNNING PRODUCT SEARCH SERVICE")
    print("=" * 60)

    search_service = ProductSearchService()

    try:

        result = search_service.search(data)

    except Exception as exc:

        print("=" * 60)
        print("SEARCH SERVICE ERROR")
        print("=" * 60)
        print(exc)

        return

    # =========================================================
    # STEP 4 — FINAL RESULT
    # =========================================================

    print("=" * 60)
    print("FINAL SEARCH RESULT")
    print("=" * 60)

    print("Needs database:", result["needs_database"])
    print("Fallback used:", result["fallback_used"])
    print("Requested branch:", result["requested_branch"])

    print()

    products = result["products"]

    if not products:

        print("No products found.")

        return

    print(f"Found {len(products)} unique product(s).")

    for index, product in enumerate(
        products,
        start=1,
    ):

        print()
        print(f"PRODUCT {index}")
        print("-" * 60)

        print("Product ID:", product["productid"])
        print("SKU:", product["sku"])
        print("\nFULL PRODUCT DATA:")
        print(product)
        print("Name:", product["productname"])
        print("Brand:", product["productbrand"])
        print("Model:", product["productmodel"])
        print("Price:", product["productprice"])
        print("Gender:", product["productgender"])
        print("Category:", product["productcategory"])
        print("Usage:", product["productusage"])
        print("Size:", product["productsize"])

        print()
        print("AVAILABLE BRANCHES:")

        for branch in product["branches"]:

            print(
                f"  - {branch['branchname']} "
                f"({branch['city']}) "
                f"| Quantity: {branch['quantity']}"
            )


if __name__ == "__main__":
    main()