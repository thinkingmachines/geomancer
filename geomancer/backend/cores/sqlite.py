# -*- coding: utf-8 -*-

# Import standard library
import sqlite3
import uuid

# Import modules
from loguru import logger
from sqlalchemy import create_engine, event
from sqlalchemy.sql import func

from .base import DBCore


class SQLiteCore(DBCore):
    """SQLite Core with Spatialite Extension"""

    def __init__(self, dburl, options=None):
        super(SQLiteCore, self).__init__(dburl, options)

    def ST_GeoFromText(self, x):
        return func.ST_GeomFromText(x, 4326)

    def load(
        self, df, index_label=None, index=False, if_exists="replace", **kwargs
    ):
        """Upload a pandas.DataFrame inside SQLite with a unique 32-char ID"""

        # Generate a unique table_id for every dataframe upload job
        table_id = uuid.uuid4().hex
        conn = sqlite3.connect(self.dburl.database)

        # Here we're mimicking BQ client by implicitly creating a column
        # __index_level_0__ via the pyarrow dependency
        df = df.reset_index()
        df = df.rename(columns={"index": "__index_level_0__"})

        # Load dataframe into SQL table
        df.to_sql(table_id, con=conn, index=index, if_exists=if_exists)

        return table_id

    def _load_spatialite(self, conn):
        """Load mod_spatialite or libspatialite"""

        try:
            conn.load_extension("mod_spatialite")
            logger.trace("Using mod_spatialite")
        except sqlite3.OperationalError:
            conn.load_extension("libspatialite")
            logger.trace("Using libspatialite")

    def _connection_listener(self, conn, record):
        """Loads spatialite whenever a connection is detected"""
        conn.enable_load_extension(True)
        self._load_spatialite(conn)

    def get_engine(self):
        """Get the engine from the DBCore and load spatialite"""
        engine = create_engine(self.dburl)
        event.listen(engine, "connect", self._connection_listener)
        return engine
