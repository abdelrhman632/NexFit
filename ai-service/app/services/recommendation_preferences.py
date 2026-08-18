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