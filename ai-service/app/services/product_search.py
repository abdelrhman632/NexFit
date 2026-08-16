from app.database.sql_builder import SQLBuilder
from app.database.query_executor import QueryExecutor


class ProductSearchService:

    def __init__(self):
        self.builder = SQLBuilder()
        self.executor = QueryExecutor()

    def search(self, filters):
        """
        Search using all requested filters, including branch.
        """

        sql = self.builder.build(
            filters,
            include_branch=True,
        )

        results = self.executor.execute(sql)

        return results

    def search_without_branch(self, filters):
        """
        Search using all requested filters except branch.
        """

        sql = self.builder.build(
            filters,
            include_branch=False,
        )

        results = self.executor.execute(sql)

        return results