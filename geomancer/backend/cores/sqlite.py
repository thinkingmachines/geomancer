# -*- coding: utf-8 -*-

# Import standard library
import sqlite3
import uuid

from .base import DBCore


class SQLiteCore(DBCore):
    """SQLite Core with Spatialite Extension"""

    def __init__(self, path):
        """Initialite the database core

        Parameters
        ----------
        path : str
            Local path to the SQLite database
        """
        super(SQLiteCore, self).__init__()
        self.path = path
        self.prefix = "sqlite:///{}"
        self.database_uri = self.prefix.format(self.path)

    def load(self, df, index_label=None, index=False, if_exists="replace"):
        """Upload a pandas.DataFrame inside SQLite with a unique 32-char ID"""

        # Generate a unique table_id for every dataframe upload job
        table_id = uuid.uuid4().hex
        conn = sqlite3.connect(self.path)

        # Ensure that spatialite extension is enabled
        conn.enable_load_extension(True)
        try:
            conn.load_extension("mod_spatialite.so")
        except sqlite3.OperationalError:
            conn.load_extension("libspatialite.so")

        # Load dataframe into SQL table
        df.to_sql(table_id, con=conn, index=index, if_exists=if_exists)
        conn.close()

        return table_id
