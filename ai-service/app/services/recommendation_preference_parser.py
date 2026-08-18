from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Preference:
    desired: Any
    priority: str


@dataclass
class RecommendationPreferences:

    comfort: Optional[Preference] = None
    long_distance: Optional[Preference] = None
    lightweight: Optional[Preference] = None
    stability: Optional[Preference] = None
    cushioning: Optional[Preference] = None
    speed: Optional[Preference] = None
    breathability: Optional[Preference] = None
    waterproof: Optional[Preference] = None
    energy_return: Optional[Preference] = None
    road: Optional[Preference] = None
    trail: Optional[Preference] = None
    latest_model: Optional[Preference] = None


class RecommendationPreferenceParser:

    @staticmethod
    def _parse_preference(value):

        if value is None:
            return None

        if not isinstance(value, dict):
            return None

        desired = value.get("desired")
        priority = value.get("priority")

        if desired is None or priority is None:
            return None

        priority = str(priority).lower()

        if priority not in {
            "high",
            "medium",
            "low",
        }:
            return None

        return Preference(
            desired=desired,
            priority=priority,
        )

    def parse(self, data):

        preferences_data = data.get(
            "preferences",
            {},
        )

        return RecommendationPreferences(

            comfort=self._parse_preference(
                preferences_data.get("comfort")
            ),

            long_distance=self._parse_preference(
                preferences_data.get("long_distance")
            ),

            lightweight=self._parse_preference(
                preferences_data.get("lightweight")
            ),

            stability=self._parse_preference(
                preferences_data.get("stability")
            ),

            cushioning=self._parse_preference(
                preferences_data.get("cushioning")
            ),

            speed=self._parse_preference(
                preferences_data.get("speed")
            ),

            breathability=self._parse_preference(
                preferences_data.get("breathability")
            ),

            waterproof=self._parse_preference(
                preferences_data.get("waterproof")
            ),

            energy_return=self._parse_preference(
                preferences_data.get("energy_return")
            ),

            road=self._parse_preference(
                preferences_data.get("road")
            ),

            trail=self._parse_preference(
                preferences_data.get("trail")
            ),

            latest_model=self._parse_preference(
                preferences_data.get("latest_model")
            ),
        )