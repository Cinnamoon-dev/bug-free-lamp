import os
import psycopg2
from psycopg2._psycopg import connection, cursor
from abc import ABC, abstractmethod


class Database(ABC):
    """Database Context Manager"""

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection: connection = self.connect_to_database()
        self.cursor: cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_value is not None or exception_type is not None:
            self.connection.rollback()
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):
    """Psycopg2 Context Manager"""

    def __init__(self) -> None:
        self.driver = psycopg2
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "1234"),
            database=os.getenv("DB_NAME", "sqltest"),
        )
