from typing import Any

from app.prompts.recommendation_prompt import RECOMMENDATION_SYSTEM_PROMPT


class RecommendationEngine:

    MAX_RECOMMENDATIONS = 5

    def recommend(
        self,
        products: list[dict[str, Any]],
        filters: Any,
    ) -> list[dict[str, Any]]:
        """
        Rank eligible products according to the user's requirements.

        ProductSearchService:
            Finds eligible candidates.

        RecommendationEngine:
            Scores and ranks those candidates.

        This class does not query the database.
        """

        if not products:
            return []

        scored_products = []

        for product in products:

            score = 0
            reasons = []

            # =====================================================
            # HARD / EXPLICIT FILTER MATCHES
            # =====================================================

            requested_gender = getattr(filters, "gender", None)

            if requested_gender:
                if product.get("productgender") in requested_gender:
                    score += 20
                    reasons.append(
                        "Matches the requested gender."
                    )

            requested_category = getattr(filters, "category", None)

            if requested_category:
                if product.get("productcategory") == requested_category:
                    score += 20
                    reasons.append(
                        "Matches the requested running category."
                    )

            requested_usage = getattr(filters, "usage", None)

            if requested_usage:
                if product.get("productusage") == requested_usage:
                    score += 25
                    reasons.append(
                        "Matches the requested usage."
                    )

            requested_size = getattr(filters, "size", None)

            if requested_size is not None:
                if product.get("productsize") == requested_size:
                    score += 20
                    reasons.append(
                        "Available in the requested size."
                    )

            max_price = getattr(filters, "max_price", None)

            if max_price is not None:

                price = product.get("productprice")

                if (
                    price is not None
                    and float(price) <= float(max_price)
                ):
                    score += 10
                    reasons.append(
                        "Within the requested budget."
                    )

            # =====================================================
            # AVAILABILITY
            # =====================================================

            branches = product.get("branches", [])

            available = any(
                branch.get("quantity", 0) > 0
                for branch in branches
            )

            if available:
                score += 5
                reasons.append(
                    "Currently available in stock."
                )

            # =====================================================
            # PRODUCT SUITABILITY
            # =====================================================

            # These attributes are currently used only when they
            # directly support an explicitly requested usage.

            if requested_usage == "Long Distance":

                recommended_distance = (
                    product.get("recommendeddistance")
                )

                if recommended_distance in (
                    "Long",
                    "Ultra",
                ):
                    score += 10
                    reasons.append(
                        "Designed for longer-distance running."
                    )

                cushioning = product.get("cushioning")

                if cushioning in (
                    "High",
                    "Maximum",
                ):
                    score += 10
                    reasons.append(
                        "Provides strong cushioning for comfort."
                    )

            # =====================================================
            # SAVE RESULT
            # =====================================================

            scored_products.append(
                {
                    "product": product,
                    "score": score,
                    "reasons": reasons,
                }
            )

        # =========================================================
        # SORT BY SCORE
        # =========================================================

        scored_products.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # =========================================================
        # TOP 5
        # =========================================================

        return scored_products[
            : self.MAX_RECOMMENDATIONS
        ]