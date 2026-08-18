from typing import Any


# ============================================================
# PREFERENCE WEIGHTS
# ============================================================
#
# These weights represent the importance of each preference
# relative to the others.
#
# They add up to 100, but the engine only uses the weights
# for preferences that the user actually specified.
#
# Therefore:
#
# If user specifies 5 preferences and a product perfectly
# satisfies all 5 -> 100/100.
#
# If user specifies only 1 preference and product perfectly
# satisfies it -> 100/100.
#
# ============================================================

PREFERENCE_WEIGHTS = {
    "comfort": 15,
    "long_distance": 15,
    "lightweight": 10,
    "stability": 10,
    "cushioning": 10,
    "speed": 10,
    "breathability": 5,
    "waterproof": 5,
    "energy_return": 10,
    "road": 5,
    "trail": 3,
    "latest_model": 2,
}


PRIORITY_MULTIPLIERS = {
    "high": 1.0,
    "medium": 0.70,
    "low": 0.40,
}


# ============================================================
# HELPERS
# ============================================================

def priority_multiplier(priority: str) -> float:

    return PRIORITY_MULTIPLIERS.get(
        str(priority).lower(),
        1.0,
    )


def normalize_text(value: Any) -> str:

    if value is None:
        return ""

    return str(value).strip().lower()


# ============================================================
# ORDERED ATTRIBUTE MATCHING
# ============================================================

def ordered_match(
    actual: Any,
    desired: Any,
    priority: str,
    max_score: float,
    order: list[str],
):
    """
    Used for attributes where higher/lower values are meaningful.

    Example:

        User wants High energy return.

        Maximum -> excellent match
        High    -> perfect match
        Medium  -> partial match
        Low     -> weak match

    Importantly, a lower value is NOT universally bad.

    If the user wants Low energy return:

        Low     -> perfect
        Medium  -> partial
        High    -> weak
        Maximum -> weak
    """

    if actual is None or desired is None:

        return 0.0, 0.0

    actual = normalize_text(actual)
    desired = normalize_text(desired)

    normalized_order = [
        normalize_text(value)
        for value in order
    ]

    if actual not in normalized_order:
        return 0.0, 0.0

    if desired not in normalized_order:
        return 0.0, 0.0

    actual_index = normalized_order.index(actual)
    desired_index = normalized_order.index(desired)

    distance = abs(
        actual_index - desired_index
    )

    max_distance = len(
        normalized_order
    ) - 1

    if max_distance == 0:

        match_ratio = 1.0

    else:

        match_ratio = max(
            0.0,
            1.0 - (
                distance / max_distance
            ),
        )

    score = (
        max_score
        * match_ratio
        * priority_multiplier(priority)
    )

    return score, match_ratio


# ============================================================
# BOOLEAN MATCHING
# ============================================================

def boolean_match(
    actual: Any,
    desired: Any,
    priority: str,
    max_score: float,
):

    if actual is None or desired is None:

        return 0.0, 0.0

    actual = bool(actual)
    desired = bool(desired)

    if actual == desired:

        match_ratio = 1.0

    else:

        match_ratio = 0.0

    score = (
        max_score
        * match_ratio
        * priority_multiplier(priority)
    )

    return score, match_ratio


# ============================================================
# CATEGORICAL MATCHING
# ============================================================

def categorical_match(
    actual: Any,
    desired: Any,
    priority: str,
    max_score: float,
):

    if actual is None or desired is None:

        return 0.0, 0.0

    actual = normalize_text(actual)
    desired = normalize_text(desired)

    if actual == desired:

        match_ratio = 1.0

    else:

        # Different categorical value is not treated as
        # universally "bad".
        #
        # It simply does not satisfy this preference.
        match_ratio = 0.0

    score = (
        max_score
        * match_ratio
        * priority_multiplier(priority)
    )

    return score, match_ratio


# ============================================================
# LIGHTWEIGHT
# ============================================================

def score_lightweight(
    product: dict,
    preference,
    max_score: float,
):

    weight = product.get("weight")

    if weight is None:

        return 0.0, 0.0, []

    try:

        weight = float(weight)

    except (
        TypeError,
        ValueError,
    ):

        return 0.0, 0.0, []

    desired = normalize_text(
        preference.desired
    )

    if desired == "light":

        if weight <= 240:
            ratio = 1.0

        elif weight <= 260:
            ratio = 0.90

        elif weight <= 280:
            ratio = 0.70

        elif weight <= 300:
            ratio = 0.40

        else:
            ratio = 0.10

    elif desired == "heavy":

        if weight >= 300:
            ratio = 1.0

        elif weight >= 280:
            ratio = 0.90

        elif weight >= 260:
            ratio = 0.70

        elif weight >= 240:
            ratio = 0.40

        else:
            ratio = 0.10

    else:

        return 0.0, 0.0, []

    score = (
        max_score
        * ratio
        * priority_multiplier(
            preference.priority
        )
    )

    reasons = []

    if ratio >= 0.90:

        reasons.append(
            f"Weight of {weight:.0f}g strongly "
            f"matches the requested {preference.desired.lower()} "
            "weight preference."
        )

    elif ratio >= 0.70:

        reasons.append(
            f"Weight of {weight:.0f}g reasonably "
            f"matches the requested {preference.desired.lower()} "
            "weight preference."
        )

    else:

        reasons.append(
            f"Weight of {weight:.0f}g is less aligned "
            f"with the requested {preference.desired.lower()} "
            "weight preference."
        )

    return score, ratio, reasons


# ============================================================
# LONG DISTANCE
# ============================================================

def score_long_distance(
    product: dict,
    preference,
    max_score: float,
):

    desired = preference.desired

    if desired is not True:

        return 0.0, 0.0, []

    usage = normalize_text(
        product.get("productusage")
    )

    distance = normalize_text(
        product.get("recommendeddistance")
    )

    if usage == "long distance":

        ratio = 1.0

        reason = (
            "The shoe is specifically classified "
            "for long-distance running."
        )

    elif distance == "ultra":

        ratio = 1.0

        reason = (
            "The shoe is recommended for "
            "ultra-distance running."
        )

    elif distance == "long":

        ratio = 1.0

        reason = (
            "The shoe is recommended for "
            "long-distance running."
        )

    elif distance == "any":

        ratio = 0.70

        reason = (
            "The shoe is suitable for a broad range "
            "of running distances."
        )

    elif distance == "medium":

        ratio = 0.40

        reason = (
            "The shoe is primarily recommended "
            "for medium distances."
        )

    elif distance == "short":

        ratio = 0.20

        reason = (
            "The shoe is primarily recommended "
            "for shorter distances."
        )

    else:

        ratio = 0.0
        reason = ""

    score = (
        max_score
        * ratio
        * priority_multiplier(
            preference.priority
        )
    )

    reasons = []

    if reason:

        reasons.append(reason)

    return score, ratio, reasons


# ============================================================
# COMFORT
# ============================================================

def score_comfort(
    product: dict,
    preference,
    max_score: float,
    active_preferences: set[str],
):

    desired = normalize_text(
        preference.desired
    )

    if desired != "high":

        return 0.0, 0.0, []

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Comfort is composite.
    #
    # However, if the user explicitly requested cushioning,
    # breathability, lightweight, or stability separately,
    # we remove that attribute from the composite comfort
    # calculation to avoid double-counting it.
    # --------------------------------------------------------

    components = []

    if "cushioning" not in active_preferences:

        components.append(
            (
                "cushioning",
                product.get("cushioning"),
            )
        )

    if "breathability" not in active_preferences:

        components.append(
            (
                "breathability",
                product.get("breathability"),
            )
        )

    if "lightweight" not in active_preferences:

        components.append(
            (
                "weight",
                product.get("weight"),
            )
        )

    if "stability" not in active_preferences:

        components.append(
            (
                "support",
                product.get("supporttype"),
            )
        )

    if not components:

        return (
            max_score
            * priority_multiplier(
                preference.priority
            ),
            1.0,
            [
                "Comfort is explicitly requested, "
                "while its individual supporting "
                "attributes are being evaluated separately."
            ],
        )

    ratios = []
    reasons = []

    # --------------------------------------------------------
    # Cushioning
    # --------------------------------------------------------

    for name, value in components:

        if name == "cushioning":

            scores = {
                "maximum": 1.00,
                "high": 0.90,
                "medium": 0.60,
                "low": 0.30,
            }

            ratio = scores.get(
                normalize_text(value),
                0.0,
            )

            ratios.append(ratio)

            if ratio >= 0.90:

                reasons.append(
                    f"{value} cushioning strongly "
                    "supports the user's comfort preference."
                )

        # ----------------------------------------------------
        # Breathability
        # ----------------------------------------------------

        elif name == "breathability":

            scores = {
                "high": 1.00,
                "medium": 0.70,
                "low": 0.30,
            }

            ratio = scores.get(
                normalize_text(value),
                0.0,
            )

            ratios.append(ratio)

            if ratio >= 0.90:

                reasons.append(
                    "High breathability supports "
                    "the user's comfort preference."
                )

        # ----------------------------------------------------
        # Weight
        # ----------------------------------------------------

        elif name == "weight":

            if value is None:

                ratio = 0.0

            else:

                try:

                    weight = float(value)

                    if weight <= 240:
                        ratio = 1.00

                    elif weight <= 260:
                        ratio = 0.90

                    elif weight <= 280:
                        ratio = 0.75

                    elif weight <= 300:
                        ratio = 0.60

                    else:
                        ratio = 0.40

                except (
                    TypeError,
                    ValueError,
                ):

                    ratio = 0.0

            ratios.append(ratio)

        # ----------------------------------------------------
        # Support
        # ----------------------------------------------------

        elif name == "support":

            support = normalize_text(value)

            if support in (
                "neutral",
                "stability",
            ):

                ratio = 1.0

            else:

                ratio = 0.0

            ratios.append(ratio)

    if not ratios:

        return 0.0, 0.0, []

    average_ratio = (
        sum(ratios) / len(ratios)
    )

    score = (
        max_score
        * average_ratio
        * priority_multiplier(
            preference.priority
        )
    )

    return (
        score,
        average_ratio,
        reasons,
    )


# ============================================================
# SPEED
# ============================================================

def score_speed(
    product: dict,
    preference,
    max_score: float,
):

    desired = normalize_text(
        preference.desired
    )

    if desired != "high":

        return 0.0, 0.0, []

    usage = normalize_text(
        product.get("productusage")
    )

    energy = normalize_text(
        product.get("energyreturn")
    )

    if usage in (
        "speed training",
        "racing",
    ):

        ratio = 1.0

        reason = (
            "The shoe is designed for "
            "speed-oriented running."
        )

    elif energy == "maximum":

        ratio = 0.85

        reason = (
            "Maximum energy return supports "
            "a responsive running experience."
        )

    elif energy == "high":

        ratio = 0.75

        reason = (
            "High energy return supports "
            "a responsive running experience."
        )

    else:

        ratio = 0.30
        reason = ""

    score = (
        max_score
        * ratio
        * priority_multiplier(
            preference.priority
        )
    )

    reasons = []

    if reason:

        reasons.append(reason)

    return score, ratio, reasons


# ============================================================
# ROAD / TRAIL
# ============================================================

def score_terrain(
    product: dict,
    preference,
    desired_terrain: str,
    max_score: float,
):

    desired = preference.desired

    if desired is not True:

        return 0.0, 0.0, []

    surface = normalize_text(
        product.get("surface")
    )

    terrain = normalize_text(
        product.get("terrain")
    )

    actual = (
        surface == desired_terrain
        or terrain == desired_terrain
    )

    ratio = 1.0 if actual else 0.0

    score = (
        max_score
        * ratio
        * priority_multiplier(
            preference.priority
        )
    )

    reasons = []

    if actual:

        reasons.append(
            f"The shoe is suitable for "
            f"{desired_terrain} running."
        )

    return score, ratio, reasons


# ============================================================
# MAIN SCORER
# ============================================================

def score_preference(
    product: dict,
    preference_name: str,
    preference,
    active_preferences: set[str],
):

    max_score = PREFERENCE_WEIGHTS.get(
        preference_name,
        0,
    )

    if preference is None:

        return {
            "score": 0.0,
            "max_score": 0.0,
            "ratio": 0.0,
            "reasons": [],
        }

    # ========================================================
    # COMFORT
    # ========================================================

    if preference_name == "comfort":

        score, ratio, reasons = score_comfort(
            product,
            preference,
            max_score,
            active_preferences,
        )

    # ========================================================
    # LONG DISTANCE
    # ========================================================

    elif preference_name == "long_distance":

        score, ratio, reasons = score_long_distance(
            product,
            preference,
            max_score,
        )

    # ========================================================
    # LIGHTWEIGHT
    # ========================================================

    elif preference_name == "lightweight":

        score, ratio, reasons = score_lightweight(
            product,
            preference,
            max_score,
        )

    # ========================================================
    # CUSHIONING
    # ========================================================

    elif preference_name == "cushioning":

        score, ratio = ordered_match(
            product.get("cushioning"),
            preference.desired,
            preference.priority,
            max_score,
            [
                "Low",
                "Medium",
                "High",
                "Maximum",
            ],
        )

        reasons = []

        if ratio >= 0.90:

            reasons.append(
                f"{product.get('cushioning')} cushioning "
                "matches the user's requested level."
            )

    # ========================================================
    # ENERGY RETURN
    # ========================================================

    elif preference_name == "energy_return":

        score, ratio = ordered_match(
            product.get("energyreturn"),
            preference.desired,
            preference.priority,
            max_score,
            [
                "Low",
                "Medium",
                "High",
                "Maximum",
            ],
        )

        reasons = []

        if ratio >= 0.90:

            reasons.append(
                f"{product.get('energyreturn')} energy return "
                "matches the user's requested level."
            )

    # ========================================================
    # BREATHABILITY
    # ========================================================

    elif preference_name == "breathability":

        score, ratio = ordered_match(
            product.get("breathability"),
            preference.desired,
            preference.priority,
            max_score,
            [
                "Low",
                "Medium",
                "High",
            ],
        )

        reasons = []

        if ratio >= 0.90:

            reasons.append(
                "Breathability matches the user's "
                "requested level."
            )

    # ========================================================
    # STABILITY
    # ========================================================

    elif preference_name == "stability":

        score, ratio = categorical_match(
            product.get("supporttype"),
            preference.desired,
            preference.priority,
            max_score,
        )

        reasons = []

        if ratio == 1.0:

            reasons.append(
                "The shoe's support type matches "
                "the user's stability preference."
            )

    # ========================================================
    # SPEED
    # ========================================================

    elif preference_name == "speed":

        score, ratio, reasons = score_speed(
            product,
            preference,
            max_score,
        )

    # ========================================================
    # WATERPROOF
    # ========================================================

    elif preference_name == "waterproof":

        score, ratio = boolean_match(
            product.get("waterproof"),
            preference.desired,
            preference.priority,
            max_score,
        )

        reasons = []

        if ratio == 1.0:

            if preference.desired is True:

                reasons.append(
                    "The shoe is waterproof as requested."
                )

            else:

                reasons.append(
                    "The shoe is non-waterproof, "
                    "matching the user's explicit preference."
                )

    # ========================================================
    # ROAD
    # ========================================================

    elif preference_name == "road":

        score, ratio, reasons = score_terrain(
            product,
            preference,
            "road",
            max_score,
        )

    # ========================================================
    # TRAIL
    # ========================================================

    elif preference_name == "trail":

        score, ratio, reasons = score_terrain(
            product,
            preference,
            "trail",
            max_score,
        )

    # ========================================================
    # LATEST MODEL
    # ========================================================

    elif preference_name == "latest_model":

        # Latest-model scoring requires comparing all
        # candidates against each other.
        #
        # This will be handled by the recommendation engine.
        #
        return {
            "score": 0.0,
            "max_score": max_score,
            "ratio": 0.0,
            "reasons": [],
        }

    else:

        return {
            "score": 0.0,
            "max_score": 0.0,
            "ratio": 0.0,
            "reasons": [],
        }

    return {
        "score": score,
        "max_score": max_score,
        "ratio": ratio,
        "reasons": reasons,
    }