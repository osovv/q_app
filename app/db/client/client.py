from typing import Any

import sqlalchemy

from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError


class PostgreSQLConnection:

    def __init__(self, host: str, port: int, user: str, password: str, db_name: str, rebuild_db: bool = False):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.rebuild_db = rebuild_db
        self.connection = self.connect()

        session = sessionmaker(
            bind=self.connection.engine,
            autocommit=True,
            autoflush=True,
            enable_baked_queries=False,
            expire_on_commit=True
        )

        self.session = session()

    def get_connection(self, db_created: bool = False) -> Any:
        engine = sqlalchemy.create_engine(
            f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name if db_created else ""}',
            encoding='utf8'
        )
        return engine.connect()

    def connect(self) -> Any:
        # if self.rebuild_db:
        #     connection.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
        #     connection.execute(f'CREATE DATABASE {self.db_name}')
        return self.get_connection(db_created=True)

    def execute_query(self, query) -> Any:
        res = self.connection.execute(query)
        return res
