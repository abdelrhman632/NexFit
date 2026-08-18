from app.services.filter_parser import FilterParser
from app.services.filter_validator import FilterValidator
from app.services.result_aggregator import ResultAggregator

from app.database.sql_builder import SQLBuilder
from app.database.sql_validator import validate_sql
from app.database.query_executor import QueryExecutor


class ProductSearchService:

    def __init__(self):
        self.filter_parser = FilterParser()
        self.filter_validator = FilterValidator()
        self.result_aggregator = ResultAggregator()

        self.builder = SQLBuilder()
        self.executor = QueryExecutor()

    def search(self, data: dict) -> dict:

        # =====================================================
        # 1. Check whether database is required
        # =====================================================

        if not data.get("needs_database", False):

            return {
                "needs_database": False,
                "products": [],
                "fallback_used": False,
                "requested_branch": None,
                "message": data.get("reason"),
            }

        # =====================================================
        # 2. Make sure Gemini returned filters
        # =====================================================

        if not data.get("filters"):

            raise ValueError(
                "Gemini returned no search filters."
            )

        # =====================================================
        # 3. Gemini JSON → SearchFilters
        # =====================================================

        filters = self.filter_parser.parse(data)

        # =====================================================
        # 4. Validate SearchFilters
        # =====================================================

        filters = self.filter_validator.validate(filters)

        # =====================================================
        # 5. Primary search
        # =====================================================

        primary_rows = self._execute_search(
            filters,
            include_branch=True,
        )

        primary_products = self.result_aggregator.aggregate(
            primary_rows
        )

        # =====================================================
        # 6. Exact matches found
        # =====================================================

        if primary_products:

            return {
                "needs_database": True,
                "products": primary_products,
                "fallback_used": False,
                "requested_branch": filters.branch,
            }

        # =====================================================
        # 7. No branch → no fallback
        # =====================================================

        if not filters.branch:

            return {
                "needs_database": True,
                "products": [],
                "fallback_used": False,
                "requested_branch": None,
            }

        # =====================================================
        # 8. Location fallback
        # =====================================================

        fallback_rows = self._execute_search(
            filters,
            include_branch=False,
        )

        fallback_products = self.result_aggregator.aggregate(
            fallback_rows
        )

        # =====================================================
        # 9. Final result
        # =====================================================

        return {
            "needs_database": True,
            "products": fallback_products,
            "fallback_used": True,
            "requested_branch": filters.branch,
        }

    def _execute_search(
        self,
        filters,
        include_branch: bool,
    ) -> list[dict]:
        """
        Build, validate, and execute a database search.
        """

        # =====================================================
        # Build SQL
        # =====================================================

        sql = self.builder.build(
            filters,
            include_branch=include_branch,
        )

        # =====================================================
        # Validate SQL
        # =====================================================

        valid, message = validate_sql(sql)

        if not valid:

            raise ValueError(
                f"SQL validation failed: {message}"
            )

        # =====================================================
        # Execute SQL
        # =====================================================

        return self.executor.execute(sql)   