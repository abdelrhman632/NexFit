from typing import Any


class RecommendationEngine:

    MAX_RECOMMENDATIONS = 5

    def recommend(
        self,
        products: list[dict[str, Any]],
        filters: Any,
    ) -> list[dict[str, Any]]:
        """
        Rank candidate products according to the user's requested filters.

        ProductSearchService is responsible for finding valid candidates.
        RecommendationEngine is responsible for ranking those candidates.
        """

        if not products:
            return []

        scored_products = []

        for product in products:
            score = 0
            reasons = []

            # =========================================================
            # 1. GENDER
            # =========================================================

            requested_gender = getattr(filters, "gender", None)

            if requested_gender:
                product_gender = product.get("productgender")

                if product_gender in requested_gender:
                    score += 20
                    reasons.append("Matches the requested gender.")

            # =========================================================
            # 2. CATEGORY
            # =========================================================

            requested_category = getattr(filters, "category", None)

            if requested_category:
                if product.get("productcategory") == requested_category:
                    score += 20
                    reasons.append("Matches the requested product category.")

            # =========================================================
            # 3. USAGE
            # =========================================================

            requested_usage = getattr(filters, "usage", None)

            if requested_usage:
                if product.get("productusage") == requested_usage:
                    score += 25
                    reasons.append("Matches the requested usage.")

            # =========================================================
            # 4. SIZE
            # =========================================================

            requested_size = getattr(filters, "size", None)

            if requested_size is not None:
                if product.get("productsize") == requested_size:
                    score += 20
                    reasons.append("Available in the requested size.")

            # =========================================================
            # 5. PRICE
            # =========================================================

            max_price = getattr(filters, "max_price", None)

            if max_price is not None:
                price = product.get("productprice")

                if price is not None and float(price) <= float(max_price):
                    score += 10
                    reasons.append("Within the requested budget.")

            # =========================================================
            # 6. AVAILABILITY
            # =========================================================

            quantity = product.get("quantity")

            if quantity is not None and quantity > 0:
                score += 5
                reasons.append("Currently available in stock.")

            # =========================================================
            # SAVE SCORE
            # =========================================================

            scored_products.append(
                {
                    "product": product,
                    "score": score,
                    "reasons": reasons,
                }
            )

        # =============================================================
        # SORT
        # =============================================================

        scored_products.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # =============================================================
        # TOP 5
        # =============================================================

        return scored_products[: self.MAX_RECOMMENDATIONS]