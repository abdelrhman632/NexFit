from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchFilters:

    # =====================================================
    # PRODUCT IDENTITY
    # =====================================================

    brand: Optional[str] = None

    model: Optional[str] = None

    # =====================================================
    # BASIC FILTERS
    # =====================================================

    gender: Optional[list[str]] = None

    category: Optional[str] = None

    usage: Optional[str] = None

    size: Optional[int] = None

    # =====================================================
    # PRICE
    # =====================================================

    max_price: Optional[float] = None

    min_price: Optional[float] = None

    # =====================================================
    # LOCATION
    # =====================================================

    branch: Optional[str] = None