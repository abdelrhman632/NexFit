from app.services.search_filters import SearchFilters


class FilterParser:

    def parse(self, data: dict) -> SearchFilters:

        filters = data.get("filters", {})

        return SearchFilters(
            gender=self._parse_gender(filters.get("gender")),
            category=self._parse_string(filters.get("category")),
            usage=self._parse_string(filters.get("usage")),
            size=self._parse_size(filters.get("size")),
            max_price=self._parse_number(filters.get("max_price")),
            min_price=self._parse_number(filters.get("min_price")),
            branch=self._parse_string(filters.get("branch")),
        )

    def _parse_gender(self, value):

        if value is None:
            return None

        if isinstance(value, str):
            return [value]

        if isinstance(value, list):
            return value

        raise ValueError("Gender must be a string or list.")

    def _parse_string(self, value):

        if value is None:
            return None

        if not isinstance(value, str):
            raise ValueError(
                f"Expected string but received {type(value).__name__}."
            )

        value = value.strip()

        if not value:
            return None

        return value

    def _parse_size(self, value):

        if value is None:
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, str):

            value = value.strip()

            if value.isdigit():
                return int(value)

        raise ValueError("Size must be an integer.")

    def _parse_number(self, value):

        if value is None:
            return None

        if isinstance(value, (int, float)):
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
            f"Expected numeric value but received {type(value).__name__}."
        )