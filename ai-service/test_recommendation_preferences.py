import json

from app.services.llm import LLMService
from app.services.recommendation_preference_parser import (
    RecommendationPreferenceParser,
)


def run_test(test_number, user_text):

    print("=" * 60)
    print(f"TEST {test_number}")
    print("=" * 60)

    print("USER REQUEST")
    print(user_text)

    # =========================================================
    # STEP 1 — GEMINI
    # =========================================================

    print("=" * 60)
    print("GENERATING RECOMMENDATION PREFERENCES")
    print("=" * 60)

    llm = LLMService()

    response = llm.generate_recommendation_preferences(
        user_text
    )

    print(response)

    # =========================================================
    # STEP 2 — JSON PARSING
    # =========================================================

    print("=" * 60)
    print("PARSING GEMINI RESPONSE")
    print("=" * 60)

    data = json.loads(response)

    print(data)

    # =========================================================
    # STEP 3 — VALIDATION / PARSING
    # =========================================================

    print("=" * 60)
    print("PARSING RECOMMENDATION PREFERENCES")
    print("=" * 60)

    preferences = (
        RecommendationPreferenceParser()
        .parse(data)
    )

    print(preferences)

    print()


def main():

    # =========================================================
    # TEST 1
    # =========================================================

    run_test(
        1,
        """
أنا عايز جزمة جري مريحة جداً ومناسبة للمسافات الطويلة.
مش فارق معايا الوزن أو الموديل الجديد.
""",
    )

    # =========================================================
    # TEST 2
    # =========================================================

    run_test(
        2,
        """
عايز جزمة جري خفيفة وسريعة للـ road running.
الأهم عندي إنها تكون خفيفة وتدي energy return كويس.
""",
    )

    # =========================================================
    # TEST 3
    # =========================================================

    run_test(
        3,
        """
عايز جزمة جري رجالي مقاس 42
وبسعر أقل من 8000 جنيه.
""",
    )


if __name__ == "__main__":
    main()