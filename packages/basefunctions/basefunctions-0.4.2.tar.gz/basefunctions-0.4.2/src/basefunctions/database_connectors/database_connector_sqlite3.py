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
import sqlite3
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
PRIMARYKEYREPLACEMENT = "INTEGER PRIMARY KEY AUTOINCREMENT"


# -------------------------------------------------------------
# CLASS DEFINITIONS
# -------------------------------------------------------------
class DataBaseConnectorSQLite3(basefunctions.DataBaseConnector):
    """
    This class connects to a sqlite3 database
    In the configuration you must provide the following parameters:

    - filename: the filename of the database, default is test.db
    """

    connection = None
    connected_flag = False

    def connect(self, config: dict, *arg, **kwargs) -> Any:
        """
        connect to a sqlite3 database
        """
        filename = config.get("filename", "test.db")
        self.connection = sqlite3.connect(filename)
        self.connected_flag = True
        return self.connection

    def disconnect(self) -> None:
        """
        disconnect from a sqlite3 database
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.connected_flag = False

    def is_connected(self) -> bool:
        """
        check if a sqlite3 database is connected
        """
        return self.connected_flag

    def execute(self, query: str) -> Any:
        """
        execute a query
        """
        query = query.replace("<PRIMARYKEY>", PRIMARYKEYREPLACEMENT)
        if self.connected_flag:
            cursor = self.connection.cursor()
            cursor.executescript(query)
            return cursor.fetchall()
        else:
            return None

    def check_if_table_exists(self, table_name: str) -> bool:
        """
        check if a table exists in a sqlite3 database
        """
        if self.connected_flag:
            cursor = self.connection.cursor()
            cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            )
            return bool(cursor.fetchall())
        return False
