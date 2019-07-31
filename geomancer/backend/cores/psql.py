#-*- coding: utf-8 -*-

# Import standard library
import datetime
import time
import uuid

# Import modules
import pytz
from loguru import logger
from sqlalchemy import func

from .base import DBCore


class PostgreSQLCore(DBCore):

    def __init__(self, dburl, options=None):
        super(PostgreSQLCore, self).__init__(dburl, options)

    def ST_GeoFromText(self, x):
        return func.ST_GeogFromText(x)

    def load(
        self, df, index_label=None, index=False, if_exists="replace", **kwargs
    ):
        """Upload a pandas.DataFrame inside SQLite with a unique 32-char ID"""

        # Generate a unique table_id for every dataframe upload job
        table_id = uuid.uuid4().hex

        # Here we're mimicking BQ client by implicitly creating a column
        # __index_level_0__ via the pyarrow dependency
        df = df.reset_index()
        df = df.rename(columns={"index": "__index_level_0__"})

        # Load dataframe into SQL table
        df.to_sql(table_id, self.get_engine(), index=index, if_exists=if_exists)

        return table_id
