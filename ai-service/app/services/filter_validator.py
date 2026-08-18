from app.services.search_filters import SearchFilters


ALLOWED_GENDERS = {
    "Boys",
    "Girls",
    "Kids",
    "Men",
    "Unisex",
    "Women",
}

ALLOWED_CATEGORIES = {
    "Basketball",
    "Boots",
    "Football",
    "Hiking",
    "Kids",
    "Lifestyle",
    "Running",
    "Sandals",
    "Skateboarding",
    "Tennis",
    "Trail Running",
    "Training",
    "Walking",
}

ALLOWED_USAGES = {
    "Backpacking",
    "Casual",
    "Commuting",
    "Daily Running",
    "Fast Hiking",
    "Firm Ground",
    "Game",
    "Gym",
    "HIIT",
    "Hiking",
    "Lifestyle",
    "Long Distance",
    "Match",
    "Outdoor",
    "Racing",
    "Recovery",
    "Running",
    "Skate",
    "Speed Training",
    "Trail Racing",
    "Trail Running",
    "Walking",
    "Weightlifting",
}

ALLOWED_SIZES = {
    39,
    40,
    41,
    42,
    43,
    44,
    45,
}

ALLOWED_BRANCHES = {
    "Nasr City Branch",
    "Heliopolis Branch",
    "New Cairo Branch",
    "Tahrir Branch",
    "Rehab Branch",
    "Maadi Branch",
    "Downtown Cairo Branch",
    "Zamalek Branch",
    "October Branch",
    "Sheikh Zayed Branch",
    "Mohandessin Branch",
    "Dokki Branch",
    "Alexandria Branch",
    "Smouha Branch",
    "Mansoura Branch",
    "Tanta Branch",
    "Ismailia Branch",
    "Suez Branch",
    "Hurghada Branch",
    "Sharm El Sheikh Branch",
    "Banha Branch",
    "Zagazig Branch",
    "Damietta Branch",
    "Port Said Branch",
    "Kafr El Sheikh Branch",
    "Damanhur Branch",
    "Beni Suef Branch",
    "Fayoum Branch",
    "Minya Branch",
    "Assiut Branch",
    "Sohag Branch",
    "Qena Branch",
    "Luxor Branch",
    "Aswan Branch",
    "Marsa Matrouh Branch",
    "North Coast Branch",
    "El Gouna Branch",
    "6th October Branch",
    "Obour Branch",
    "El Shorouk Branch",
}


class FilterValidationError(ValueError):
    pass


class FilterValidator:

    def validate(self, filters: SearchFilters) -> SearchFilters:

        self._validate_gender(filters)
        self._validate_category(filters)
        self._validate_usage(filters)
        self._validate_size(filters)
        self._validate_price(filters)
        self._validate_branch(filters)

        return filters

    def _validate_gender(self, filters: SearchFilters):

        if filters.gender is None:
            return

        if not isinstance(filters.gender, list):
            raise FilterValidationError(
                "Gender must be a list."
            )

        for gender in filters.gender:
            if gender not in ALLOWED_GENDERS:
                raise FilterValidationError(
                    f"Invalid gender: {gender}"
                )

    def _validate_category(self, filters: SearchFilters):

        if filters.category is None:
            return

        if filters.category not in ALLOWED_CATEGORIES:
            raise FilterValidationError(
                f"Invalid category: {filters.category}"
            )

    def _validate_usage(self, filters: SearchFilters):

        if filters.usage is None:
            return

        if filters.usage not in ALLOWED_USAGES:
            raise FilterValidationError(
                f"Invalid usage: {filters.usage}"
            )

    def _validate_size(self, filters: SearchFilters):

        if filters.size is None:
            return

        if not isinstance(filters.size, int):
            raise FilterValidationError(
                "Size must be an integer."
            )

        if filters.size not in ALLOWED_SIZES:
            raise FilterValidationError(
                f"Invalid size: {filters.size}"
            )

    def _validate_price(self, filters: SearchFilters):

        if filters.max_price is not None:
            if not isinstance(filters.max_price, (int, float)):
                raise FilterValidationError(
                    "Maximum price must be numeric."
                )

            if filters.max_price <= 0:
                raise FilterValidationError(
                    "Maximum price must be greater than zero."
                )

        if filters.min_price is not None:
            if not isinstance(filters.min_price, (int, float)):
                raise FilterValidationError(
                    "Minimum price must be numeric."
                )

            if filters.min_price < 0:
                raise FilterValidationError(
                    "Minimum price cannot be negative."
                )

        if (
            filters.min_price is not None
            and filters.max_price is not None
            and filters.min_price > filters.max_price
        ):
            raise FilterValidationError(
                "Minimum price cannot be greater than maximum price."
            )

    def _validate_branch(self, filters: SearchFilters):

        if filters.branch is None:
            return

        if filters.branch not in ALLOWED_BRANCHES:
            raise FilterValidationError(
                f"Invalid branch: {filters.branch}"
            )