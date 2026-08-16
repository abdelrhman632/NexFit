from app.services.product_search import ProductSearchService
from app.services.recommendation_engine import RecommendationEngine


def print_product(product, rank, score, reasons):

    print("=" * 60)
    print(f"RECOMMENDATION #{rank}")
    print("=" * 60)

    print(f"Product ID: {product.get('productid')}")
    print(f"SKU: {product.get('sku')}")
    print(f"Name: {product.get('productname')}")
    print(f"Brand: {product.get('productbrand')}")
    print(f"Model: {product.get('productmodel')}")
    print(f"Price: {product.get('productprice')}")
    print(f"Gender: {product.get('productgender')}")
    print(f"Category: {product.get('productcategory')}")
    print(f"Usage: {product.get('productusage')}")
    print(f"Size: {product.get('productsize')}")

    print(f"\nRECOMMENDATION SCORE: {score}")

    print("\nWHY RECOMMENDED:")

    for reason in reasons:
        print(f"  - {reason}")

    print()


def main():

    # =========================================================
    # USER REQUEST
    # =========================================================

    print("=" * 60)
    print("USER REQUEST")
    print("=" * 60)

    user_text = """
أنا عايز حذاء جري رجالي.
مقاس 42.
ميزانيتي لحد 10000 جنيه.
عايز حاجة مريحة ومناسبة للجري.
ويفضل تكون موجودة في فرع مدينة نصر.
"""

    print(user_text)

    # =========================================================
    # STEP 1 — GEMINI DATA
    # =========================================================

    data = {
        "needs_database": True,
        "filters": {
            "gender": ["Men", "Unisex"],
            "category": "Running",
            "usage": None,
            "size": 42,
            "max_price": 10000,
            "min_price": None,
            "branch": "Nasr City Branch",
        },
        "reason": (
            "User wants a men's or unisex running shoe "
            "in size 42 under 10000 EGP, preferably "
            "available at Nasr City Branch."
        ),
    }

    print("=" * 60)
    print("GEMINI DATA")
    print("=" * 60)

    print(data)

    # =========================================================
    # STEP 2 — PRODUCT SEARCH
    # =========================================================

    print("=" * 60)
    print("RUNNING PRODUCT SEARCH SERVICE")
    print("=" * 60)

    search_service = ProductSearchService()

    search_result = search_service.search(data)

    # =========================================================
    # STEP 3 — DISPLAY SEARCH RESULT
    # =========================================================

    print("=" * 60)
    print("SEARCH RESULT")
    print("=" * 60)

    print(f"Needs database: {search_result.get('needs_database')}")
    print(f"Fallback used: {search_result.get('fallback_used')}")
    print(f"Requested branch: {search_result.get('requested_branch')}")

    products = search_result.get("products", [])

    print(f"\nFound {len(products)} candidate product(s).")

    for product in products:

        print(
            f"- {product.get('productname')} "
            f"| SKU: {product.get('sku')} "
            f"| {product.get('productprice')} EGP"
        )

    # =========================================================
    # STEP 4 — RECOMMENDATION ENGINE
    # =========================================================

    print("=" * 60)
    print("RUNNING RECOMMENDATION ENGINE")
    print("=" * 60)

    engine = RecommendationEngine()

    # The ProductSearchService has already converted the
    # Gemini filters into SearchFilters internally.
    #
    # For now we use the same original filter data for
    # the recommendation engine.

    filters = search_result.get("filters")

    recommendations = engine.recommend(
        products=products,
        filters=filters,
    )

    # =========================================================
    # STEP 5 — FINAL RECOMMENDATIONS
    # =========================================================

    print("=" * 60)
    print("FINAL RECOMMENDATIONS")
    print("=" * 60)

    print(
        f"Found {len(recommendations)} recommendation(s)."
    )

    for rank, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        print_product(
            product=recommendation["product"],
            rank=rank,
            score=recommendation["score"],
            reasons=recommendation["reasons"],
        )


if __name__ == "__main__":
    main()