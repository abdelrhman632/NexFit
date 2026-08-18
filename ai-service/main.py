import json

from app.services.llm import LLMService
from app.services.product_search import ProductSearchService


# ============================================================
# HELPERS
# ============================================================

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


def print_product(product, index):

    print()
    print(f"PRODUCT {index}")
    print("-" * 60)

    print("Product ID:", product["productid"])
    print("SKU:", product["sku"])
    print("Name:", product["productname"])
    print("Brand:", product["productbrand"])
    print("Model:", product["productmodel"])
    print("Price:", product["productprice"])
    print("Gender:", product["productgender"])
    print("Category:", product["productcategory"])
    print("Usage:", product["productusage"])
    print("Size:", product["productsize"])

    # --------------------------------------------------------
    # Full product attributes
    # --------------------------------------------------------

    print()
    print("PRODUCT SPECIFICATIONS:")

    fields = {
        "Material": "material",
        "Surface": "surface",
        "Support Type": "supporttype",
        "Cushioning": "cushioning",
        "Breathability": "breathability",
        "Weight": "weight",
        "Waterproof": "waterproof",
        "Recommended Distance": "recommendeddistance",
        "Arch Type": "archtype",
        "Foot Strike": "footstrike",
        "Energy Return": "energyreturn",
        "Release Year": "releaseyear",
        "Heel Drop": "heeldropmm",
        "Terrain": "terrain",
    }

    for label, key in fields.items():

        value = product.get(key)

        if value is not None:

            print(
                f"  {label}: {value}"
            )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    if product.get("description"):

        print()
        print("DESCRIPTION:")

        print(
            f"  {product['description']}"
        )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    print()
    print("AVAILABLE BRANCHES:")

    branches = product.get(
        "branches",
        [],
    )

    if not branches:

        print("  No branch availability.")

    else:

        for branch in branches:

            print(
                f"  - {branch['branchname']} "
                f"({branch['city']}) "
                f"| Quantity: {branch['quantity']}"
            )


# ============================================================
# RUN ONE SEARCH
# ============================================================

def run_search(
    user_text,
    llm,
    search_service,
):

    # ========================================================
    # USER REQUEST
    # ========================================================

    print()
    print("=" * 60)
    print("USER REQUEST")
    print("=" * 60)

    print(user_text)

    # ========================================================
    # STEP 1 — GEMINI
    # ========================================================

    print("=" * 60)
    print("GENERATING FILTERS WITH GEMINI")
    print("=" * 60)

    response = llm.generate_sql(
        user_text
    )

    print(response)

    # ========================================================
    # STEP 2 — PARSE GEMINI JSON
    # ========================================================

    try:

        data = parse_gemini_json(
            response
        )

    except json.JSONDecodeError as exc:

        print()
        print("=" * 60)
        print("GEMINI JSON ERROR")
        print("=" * 60)

        print(exc)

        return

    print("=" * 60)
    print("PARSED GEMINI DATA")
    print("=" * 60)

    print(data)

    # ========================================================
    # STEP 3 — PRODUCT SEARCH
    # ========================================================

    print("=" * 60)
    print("RUNNING PRODUCT SEARCH SERVICE")
    print("=" * 60)

    try:

        result = search_service.search(
            data
        )

    except Exception as exc:

        print()
        print("=" * 60)
        print("SEARCH SERVICE ERROR")
        print("=" * 60)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        return

    # ========================================================
    # STEP 4 — FINAL RESULT
    # ========================================================

    print("=" * 60)
    print("FINAL SEARCH RESULT")
    print("=" * 60)

    print(
        "Needs database:",
        result["needs_database"],
    )

    print(
        "Fallback used:",
        result["fallback_used"],
    )

    print(
        "Requested branch:",
        result["requested_branch"],
    )

    products = result.get(
        "products",
        [],
    )

    print()

    if not products:

        print("No products found.")

        return

    print(
        f"Found {len(products)} "
        f"unique product(s)."
    )

    # ========================================================
    # STEP 5 — DISPLAY PRODUCTS
    # ========================================================

    for index, product in enumerate(
        products,
        start=1,
    ):

        print_product(
            product,
            index,
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("NEXFIT AI PRODUCT SEARCH")
    print("=" * 60)

    print()
    print(
        "Enter a product request."
    )

    print(
        "Type 'exit' to close."
    )

    print()

    # --------------------------------------------------------
    # Initialize services once
    # --------------------------------------------------------

    llm = LLMService()

    search_service = (
        ProductSearchService()
    )

    # --------------------------------------------------------
    # Interactive loop
    # --------------------------------------------------------

    while True:

        try:

            user_text = input(
                "\nNexFit User > "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nClosing NexFit AI."
            )

            break

        except EOFError:

            print(
                "\n\nClosing NexFit AI."
            )

            break

        # ----------------------------------------------------
        # Empty input
        # ----------------------------------------------------

        if not user_text:

            continue

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        if user_text.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nClosing NexFit AI."
            )

            break

        # ----------------------------------------------------
        # Run complete pipeline
        # ----------------------------------------------------

        run_search(
            user_text=user_text,
            llm=llm,
            search_service=search_service,
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()