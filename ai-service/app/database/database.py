import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class DatabaseService:

    def __init__(self):

        # =====================================================
        # PRODUCTION — Railway
        # =====================================================

        self.database_url = os.getenv("DATABASE_URL")

        if self.database_url:
            self.use_database_url = True

        # =====================================================
        # LOCAL DEVELOPMENT
        # =====================================================

        else:
            self.use_database_url = False

            self.host = os.getenv(
                "DATABASE_HOST",
                "localhost",
            )

            self.port = os.getenv(
                "DATABASE_PORT",
                "5432",
            )

            self.database = os.getenv(
                "DATABASE_NAME",
            )

            self.user = os.getenv(
                "DATABASE_USER",
            )

            self.password = os.getenv(
                "DATABASE_PASSWORD",
            )

    def execute_query(self, sql: str):

        connection = None

        try:

            # =================================================
            # CONNECT TO RAILWAY
            # =================================================

            if self.use_database_url:

                connection = psycopg2.connect(
                    self.database_url
                )

            # =================================================
            # CONNECT LOCALLY
            # =================================================

            else:

                connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                )

            # =================================================
            # EXECUTE QUERY
            # =================================================

            with connection.cursor() as cursor:

                cursor.execute(sql)

                columns = [
                    description[0]
                    for description in cursor.description
                ]

                rows = cursor.fetchall()

                return [
                    dict(zip(columns, row))
                    for row in rows
                ]

        finally:

            if connection:
                connection.close()