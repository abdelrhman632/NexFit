import json

from app.services.llm import LLMService
from app.services.product_search import ProductSearchService
from app.services.recommendation_engine import RecommendationEngine
from app.services.recommendation_preference_parser import (
    RecommendationPreferenceParser,
)


def print_product(
    product,
    rank,
    score,
    reasons,
    breakdown,
    maximum_possible_score,
):

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

    print(
        f"\nRECOMMENDATION SCORE: "
        f"{score}/100"
    )

    print(
        f"MAXIMUM POSSIBLE SCORE: "
        f"{maximum_possible_score}/100"
    )

    print("\nSCORE BREAKDOWN:")

    for item in breakdown:

        print(
            f"  - {item['preference']}: "
            f"{item['score']}/{item['max_score']} "
            f"({item['match_percentage']}%)"
        )

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
أنا عايز أشتري حذاء جري رجالي من NexFit.

المواصفات الأساسية:
- مقاس 42 بالضبط.
- الميزانية القصوى 10000 جنيه.
- أريد حذاء Running.
- أريده مناسباً للجري لمسافات طويلة.
- أفضل أن يكون مريحاً جداً.
- أريد cushioning مرتفعاً، ويفضل High أو Maximum.
- أريد breathability عالية.
- لا يهمني أن يكون الحذاء خفيفاً جداً؛ الراحة أهم بالنسبة لي من الوزن.
- أريد حذاء مناسباً للجري على Road.
- لا أحتاج Waterproof.
- لا يهمني سنة الإصدار أو إذا كان الموديل جديداً.
- أفضل أن يكون متوفراً في Nasr City Branch.

رتب لي أفضل 5 أحذية من المنتجات المتاحة، وليس مجرد أرخص 5 منتجات.

في التقييم:
- أعطِ الأولوية للمواصفات التي طلبتها صراحة.
- لا تعتبر الوزن عاملاً سلبياً إذا كان المستخدم قال إن الوزن غير مهم.
- لا تعتبر سنة الإصدار عاملاً في التقييم لأنني لم أطلب أحدث موديل.
- لا تفترض أن Waterproof أفضل إذا لم أطلبه.

أريد Score من 100 لكل منتج، وسبب واضح يشرح لماذا حصل على هذا التقييم.
"""

    print(user_text)

    # =========================================================
    # STEP 1 — GENERATE SEARCH FILTERS
    # =========================================================

    print("=" * 60)
    print("GENERATING SEARCH FILTERS")
    print("=" * 60)

    llm = LLMService()

    # NOTE:
    # For now, your existing database-search pipeline
    # is still being used here.
    #
    # If your project already has a method that generates
    # the normal Gemini database JSON, use that method here.
    #
    # We keep the known working data for this test so that
    # we can focus on the recommendation engine.

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

    print(data)

    # =========================================================
    # STEP 2 — GENERATE RECOMMENDATION PREFERENCES
    # =========================================================

    print("=" * 60)
    print("GENERATING RECOMMENDATION PREFERENCES")
    print("=" * 60)

    preference_response = (
        llm.generate_recommendation_preferences(
            user_text
        )
    )

    print(preference_response)

    # =========================================================
    # STEP 3 — PARSE RECOMMENDATION PREFERENCES
    # =========================================================

    print("=" * 60)
    print("PARSING RECOMMENDATION PREFERENCES")
    print("=" * 60)

    preference_data = json.loads(
        preference_response
    )

    preferences = (
        RecommendationPreferenceParser()
        .parse(preference_data)
    )

    print(preferences)

    # =========================================================
    # STEP 4 — PRODUCT SEARCH
    # =========================================================

    print("=" * 60)
    print("RUNNING PRODUCT SEARCH SERVICE")
    print("=" * 60)

    search_service = ProductSearchService()

    search_result = search_service.search(data)

    # =========================================================
    # STEP 5 — DISPLAY SEARCH RESULT
    # =========================================================

    print("=" * 60)
    print("SEARCH RESULT")
    print("=" * 60)

    print(
        f"Needs database: "
        f"{search_result.get('needs_database')}"
    )

    print(
        f"Fallback used: "
        f"{search_result.get('fallback_used')}"
    )

    print(
        f"Requested branch: "
        f"{search_result.get('requested_branch')}"
    )

    products = search_result.get(
        "products",
        [],
    )

    print(
        f"\nFound {len(products)} "
        f"candidate product(s)."
    )

    for product in products:

        print(
            f"- {product.get('productname')} "
            f"| SKU: {product.get('sku')} "
            f"| {product.get('productprice')} EGP"
        )

    # =========================================================
    # STEP 6 — RECOMMENDATION ENGINE
    # =========================================================

    print("=" * 60)
    print("RUNNING RECOMMENDATION ENGINE")
    print("=" * 60)

    engine = RecommendationEngine()

    filters = search_result.get("filters")

    recommendations = engine.recommend(
        products=products,
        filters=filters,
        preferences=preferences,
    )

    # =========================================================
    # STEP 7 — FINAL RECOMMENDATIONS
    # =========================================================

    print("=" * 60)
    print("FINAL RECOMMENDATIONS")
    print("=" * 60)

    print(
        f"Found {len(recommendations)} "
        f"recommendation(s)."
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
    breakdown=recommendation["breakdown"],
    maximum_possible_score=recommendation[
        "maximum_possible_score"
    ],
)


if __name__ == "__main__":
    main()