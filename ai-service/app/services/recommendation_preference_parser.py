from app.services.recommendation_preferences import (
    RecommendationPreferences,
)


class RecommendationPreferenceParser:

    # These are the only priority values that Gemini is allowed
    # to return.
    ALLOWED_PRIORITIES = {
        "high",
        "medium",
        "low",
    }

    # These are the only recommendation attributes that we support.
    ALLOWED_FIELDS = {
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
    }

    def parse(self, data: dict) -> RecommendationPreferences:

        # Get the "preferences" object returned by Gemini.
        preferences = data.get("preferences", {})

        # If Gemini somehow returns something other than a dictionary,
        # safely fall back to an empty preference set.
        if not isinstance(preferences, dict):
            preferences = {}

        cleaned = {}

        # Go through our approved attributes.
        for field in self.ALLOWED_FIELDS:

            # Get Gemini's value for this attribute.
            value = preferences.get(field)

            # If Gemini returns an invalid value, discard it.
            if value not in self.ALLOWED_PRIORITIES:
                value = None

            # Store the validated value.
            cleaned[field] = value

        # Convert the validated dictionary into our typed object.
        return RecommendationPreferences(
            **cleaned
        )