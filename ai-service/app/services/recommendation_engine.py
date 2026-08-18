from typing import Any

from app.services.recommendation_scoring import (
    PREFERENCE_WEIGHTS,
    score_preference,
)


class RecommendationEngine:

    MAX_RECOMMENDATIONS = 5

    SUPPORTED_PREFERENCES = [
        "comfort",
        "long_distance",
        "lightweight",
        "stability",
        "cushioning",
        "speed",
        "breathability",
        "waterproof",
        "energy_return",
        "road",
        "trail",
        "latest_model",
    ]

    # ========================================================
    # ACTIVE PREFERENCES
    # ========================================================

    @staticmethod
    def get_active_preferences(
        preferences,
    ) -> set[str]:

        active = set()

        for name in (
            RecommendationEngine.SUPPORTED_PREFERENCES
        ):

            value = getattr(
                preferences,
                name,
                None,
            )

            if value is not None:

                active.add(name)

        return active

    # ========================================================
    # RECOMMEND
    # ========================================================

    def recommend(
        self,
        products: list[dict[str, Any]],
        filters: Any,
        preferences: Any,
    ) -> list[dict[str, Any]]:

        if not products:

            return []

        # ====================================================
        # Find what the USER ACTUALLY ASKED FOR
        # ====================================================

        active_preferences = (
            self.get_active_preferences(
                preferences
            )
        )

        if not active_preferences:

            # No recommendation preferences were specified.
            #
            # In this case, do not invent a preference.
            # Return products with neutral score.

            return [
                {
                    "product": product,
                    "score": 0.0,
                    "reasons": [
                        "No specific recommendation "
                        "preferences were provided."
                    ],
                    "breakdown": [],
                }

                for product in products[
                    :self.MAX_RECOMMENDATIONS
                ]
            ]

        # ====================================================
        # MAXIMUM POSSIBLE SCORE
        # ====================================================
        #
        # ONLY preferences explicitly requested by the user
        # contribute to the denominator.
        #
        # Example:
        #
        # comfort + road + energy_return
        #
        # Only those three weights are considered.
        #
        # A perfect product therefore gets:
        #
        # 100 / 100
        #
        # ====================================================

        maximum_possible_score = sum(
            PREFERENCE_WEIGHTS.get(
                preference_name,
                0,
            )

            for preference_name
            in active_preferences
        )

        # ====================================================
        # SCORE PRODUCTS
        # ====================================================

        scored_products = []

        for product in products:

            raw_total = 0.0

            breakdown = []

            reasons = []

            # ------------------------------------------------
            # Score every preference the user specified
            # ------------------------------------------------

            for preference_name in (
                self.SUPPORTED_PREFERENCES
            ):

                if (
                    preference_name
                    not in active_preferences
                ):

                    continue

                preference = getattr(
                    preferences,
                    preference_name,
                    None,
                )

                result = score_preference(
                    product=product,
                    preference_name=preference_name,
                    preference=preference,
                    active_preferences=active_preferences,
                )

                score = result["score"]
                max_score = result["max_score"]
                ratio = result["ratio"]

                raw_total += score

                # --------------------------------------------
                # Breakdown
                # --------------------------------------------

                breakdown.append(
                    {
                        "preference": preference_name,
                        "score": round(
                            score,
                            2,
                        ),
                        "max_score": round(
                            max_score,
                            2,
                        ),
                        "match_percentage": round(
                            ratio * 100,
                            1,
                        ),
                    }
                )

                # --------------------------------------------
                # Reasons
                # --------------------------------------------

                reasons.extend(
                    result["reasons"]
                )

            # ------------------------------------------------
            # Normalize to 100
            # ------------------------------------------------

            if maximum_possible_score > 0:

                final_score = (
                    raw_total
                    / maximum_possible_score
                ) * 100.0

            else:

                final_score = 0.0

            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            scored_products.append(
                {
                    "product": product,
                    "score": round(
                        final_score,
                        2,
                    ),
                    "raw_score": round(
                        raw_total,
                        2,
                    ),
                    "maximum_possible_score": round(
                        maximum_possible_score,
                        2,
                    ),
                    "reasons": reasons,
                    "breakdown": breakdown,
                }
            )

        # ====================================================
        # SORT
        # ====================================================

        scored_products.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # ====================================================
        # TOP 5
        # ====================================================

        return scored_products[
            :self.MAX_RECOMMENDATIONS
        ]