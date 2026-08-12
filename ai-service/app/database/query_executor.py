from app.database.sql_validator import validate_sql
from app.database.database import DatabaseService


class QueryExecutor:

    def __init__(self):
        self.database = DatabaseService()

    def execute(self, sql: str):

        valid, message = validate_sql(sql)

        if not valid:
            raise ValueError(f"SQL validation failed: {message}")

        return self.database.execute_query(sql)