from app.services.search_filters import SearchFilters


class FilterParser:

    def parse(self, data: dict) -> SearchFilters:

        filters = data.get(
            "filters",
            {}
        )

        return SearchFilters(

            # =================================================
            # PRODUCT IDENTITY
            # =================================================

            brand=self._parse_string(
                filters.get("brand")
            ),

            model=self._parse_string(
                filters.get("model")
            ),

            # =================================================
            # BASIC FILTERS
            # =================================================

            gender=self._parse_gender(
                filters.get("gender")
            ),

            category=self._parse_string(
                filters.get("category")
            ),

            usage=self._parse_string(
                filters.get("usage")
            ),

            size=self._parse_size(
                filters.get("size")
            ),

            # =================================================
            # PRICE
            # =================================================

            max_price=self._parse_number(
                filters.get("max_price")
            ),

            min_price=self._parse_number(
                filters.get("min_price")
            ),

            # =================================================
            # LOCATION
            # =================================================

            branch=self._parse_string(
                filters.get("branch")
            ),
        )

    # =========================================================
    # GENDER
    # =========================================================

    def _parse_gender(self, value):

        if value is None:
            return None

        if isinstance(value, str):

            value = value.strip()

            if not value:
                return None

            return [value]

        if isinstance(value, list):

            return [
                item.strip()
                for item in value
                if isinstance(item, str)
                and item.strip()
            ]

        raise ValueError(
            "Gender must be a string or list."
        )

    # =========================================================
    # STRING
    # =========================================================

    def _parse_string(self, value):

        if value is None:
            return None

        if not isinstance(value, str):

            raise ValueError(
                f"Expected string but received "
                f"{type(value).__name__}."
            )

        value = value.strip()

        if not value:
            return None

        return value

    # =========================================================
    # SIZE
    # =========================================================

    def _parse_size(self, value):

        if value is None:
            return None

        if isinstance(value, int):

            return value

        if isinstance(value, float):

            if value.is_integer():
                return int(value)

            raise ValueError(
                "Size must be an integer."
            )

        if isinstance(value, str):

            value = value.strip()

            if value.isdigit():

                return int(value)

        raise ValueError(
            "Size must be an integer."
        )

    # =========================================================
    # NUMBER
    # =========================================================

    def _parse_number(self, value):

        if value is None:
            return None

        if isinstance(
            value,
            (int, float)
        ):

            return value

        if isinstance(value, str):

            value = value.strip()

            try:

                return float(value)

            except ValueError:

                raise ValueError(
                    f"Invalid numeric value: {value}"
                )

        raise ValueError(
            f"Expected numeric value but received "
            f"{type(value).__name__}."
        )