from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchFilters:
    gender: Optional[list[str]] = None
    category: Optional[str] = None
    usage: Optional[str] = None
    size: Optional[int] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    branch: Optional[str] = None