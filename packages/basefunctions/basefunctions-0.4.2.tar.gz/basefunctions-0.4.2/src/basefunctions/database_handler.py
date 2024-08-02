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


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class DataBaseConnector:

    def connect(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def disconnect(self) -> None:
        raise NotImplementedError

    def is_connected(self) -> bool:
        raise NotImplementedError

    def execute(self, query: str) -> Any:
        raise NotImplementedError

    def check_if_table_exists(self, table_name: str) -> bool:
        raise NotImplementedError


class DataBaseHandler:
    """
    The DataBaseHandler class is a class to handle and abstract the database
    handling. Use the connect() method to connect to the database by providing
    either a package_name and config_name or a config dictionary. The only
    mandatory parameter is the connect_type in the configuration. The connect_type
    determines the database connector to use. The following connect_types are
    supported:
    - sqlite3
    - postgres
    Each connector has its own additional parameters, so sqlite3 just needs a
    file name, while postgres needs a protocol, host, port, user, password and
    database name.
    """

    parameters = {}
    connector = None

    def connect(
        self,
        package_name: str = None,
        config_name: str = None,
        config: dict = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Connect to the database
        """
        if package_name is not None and config_name is not None:
            self.parameters = basefunctions.ConfigHandler().get_configuration(
                package_name=package_name, config_name=config_name
            )
        elif config is not None:
            self.parameters = config
        else:
            raise ValueError("no configuration provided")
        # create database connectors
        if "connect_type" not in self.parameters:
            raise ValueError("no connect_type in configuration")
        # create database connector
        if self.parameters["connect_type"] == "sqlite3":
            self.connector = basefunctions.DataBaseConnectorSQLite3()
        elif self.parameters["connect_type"] == "postgres":
            self.connector = basefunctions.DataBaseConnectorPostgreSQL()
        else:
            raise ValueError(
                f"connector for connect_type {self.parameters['connect_type']} not found"
            )
        # connect to database
        self.connector.connect(config=self.parameters, *args, **kwargs)

    def disconnect(self):
        """
        Disconnect from the database
        """
        # disconnect from database
        if self.connector:
            self.connector.disconnect()

    def get_connection(self) -> Any:
        """
        Get the connection

        Returns:
        --------
          Any: the connection

        """
        if self.connector:
            return self.connector.connection
        return None

    def is_connected(self) -> bool:
        """
        Check if the database is connected

        Returns:
        --------
          bool: True if the database is connected, False otherwise

        """
        if self.connector:
            return self.connector.is_connected()
        return False

    def execute(self, query: str) -> Any:
        """
        Execute a query to the database

        Args:
        -----
          query (str): the query to execute

        Returns:
        --------
          Any: the result of the query

        """
        if self.connector:
            return self.connector.execute(query)
        raise ValueError("no connection to database")

    def check_if_table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database

        Args:
        -----
          table_name (str): the table name

        Returns:
        --------
          bool: True if the table exists, False otherwise

        """
        if self.connector:
            return self.connector.check_if_table_exists(table_name)
        raise ValueError("no connection to database")
