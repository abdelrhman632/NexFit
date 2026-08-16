from dataclasses import dataclass
from typing import Optional


@dataclass
class RecommendationPreferences:
    # How strongly the user cares about comfort.
    # Possible values: "high", "medium", "low", or None.
    comfort: Optional[str] = None

    # Whether long-distance suitability is important.
    long_distance: Optional[str] = None

    # Whether the user explicitly wants a lightweight shoe.
    lightweight: Optional[str] = None

    # Whether stability is important to the user.
    stability: Optional[str] = None

    # Whether cushioning is explicitly requested.
    cushioning: Optional[str] = None

    # Whether the user prioritizes speed/performance.
    speed: Optional[str] = None

    # Whether breathability is important.
    breathability: Optional[str] = None

    # Whether waterproofing is important.
    waterproof: Optional[str] = None

    # Whether high energy return is important.
    energy_return: Optional[str] = None

    # Whether the user wants a road-running shoe.
    road: Optional[str] = None

    # Whether the user wants a trail-running shoe.
    trail: Optional[str] = None

    # Whether the user specifically wants the newest/latest model.
    latest_model: Optional[str] = None