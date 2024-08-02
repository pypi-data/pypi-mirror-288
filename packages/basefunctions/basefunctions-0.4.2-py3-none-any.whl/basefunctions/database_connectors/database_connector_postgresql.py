"""
=============================================================================

  Licensed Materials, Property of Ralph Vogl, Munich

  Project : backtraderfunctions

  Copyright (c) by Ralph Vogl

  All rights reserved.

  Description:

  a simple helper package for backtrader indicators and strategies

=============================================================================
"""

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
from typing import Any
import sqlalchemy
import basefunctions

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------
PRIMARYKEYREPLACEMENT = "BIGSERIAL PRIMARY KEY"


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class DataBaseConnectorPostgreSQL(basefunctions.DataBaseConnector):
    """
    This class connects to a postgres database
    In the configuration you must provide the following parameters:

    - postgres_protocol: the protocol to use, default is postgresql+psycopg2
    - postgres_host: the host name, default is localhost
    - postgres_db: the database name, default is None
    - postgres_user: the user name, default is postgres
    - postgres_password: the password, default is None
    - postgres_port: the port, default is 5432

    """

    engine = None
    connection = None
    connected_flag = False

    def connect(self, config: dict, *args, **kwargs) -> Any:
        """
        connect to a postgresql database
        """
        sqlalchemy_protocol = config.get("postgres_protocol", "postgresql+psycopg2")
        host_name = config.get("postgres_host", "localhost")
        database_name = config.get("postgres_db", None)
        user_name = config.get("postgres_user", "postgres")
        password = config.get("postgres_password", None)
        port = config.get("postgres_port", 5432)

        self.engine = sqlalchemy.create_engine(
            f"{sqlalchemy_protocol}://{user_name}:{password}"
            f"@{host_name}:{port}/{database_name}",
        )
        self.connection = self.engine.connect()
        self.connected_flag = True

    def disconnect(self) -> None:
        """
        disconnect from the database
        """
        if self.connection and self.connected_flag:
            self.connection.dispose()
            self.connection = None
            self.connected_flag = False

    def is_connected(self) -> bool:
        """
        check if the connection is active
        """
        return self.connected_flag

    def execute(self, query: str) -> Any:
        """
        execute a query
        """
        query = query.replace("<PRIMARYKEY>", PRIMARYKEYREPLACEMENT)
        if self.connected_flag:
            return self.connection.execute(sqlalchemy.text(query))

    def check_if_table_exists(self, table_name: str) -> bool:
        """
        check if a table exists
        """
        if self.connected_flag:
            return sqlalchemy.inspect(self.connection).has_table(table_name=table_name)
        return False
