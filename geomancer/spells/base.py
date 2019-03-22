# -*- coding: utf-8 -*-

"""Base class for all feature or spell implementations

In Geomancer, all feature transform primitives are of the class :code:`Spell`.
When defining your own feature primitive, simply create a class that inherits
from :code:`Spell`:

    .. code-block:: python

        from geomancer.spells.base import Spell
        class MyNewFeature(Spell):
             def __init__(self):
                 super(MyNewFeature, self).__init__()

All methods must be implemented in order to not raise a
:code:`NotImplementedError`.
"""

# Import standard library
import abc

# Import modules
import pandas as pd
from loguru import logger
from sqlalchemy.engine.url import make_url
from sqlalchemy.sql import select

from ..backend.cores import BigQueryCore, SQLiteCore

CORES = {"bigquery": BigQueryCore, "sqlite": SQLiteCore}


class Spell(abc.ABC):
    """Base class for all feature/spell implementations"""

    @abc.abstractmethod
    def __init__(
        self,
        source_table,
        feature_name,
        source_id="osm_id",
        dburl=None,
        options=None,
    ):
        """Spell constructor

        Parameters
        ----------
        source_table : str
            Table URI to run queries against.
        feature_name : str
            Column name for the output feature.
        dburl : str, optional
            Database url used to configure backend connection
        options : :class:`geomancer.backend.settings.Config`, optional
            Specify configuration for interacting with the database backend.
            Auto-detected if not set.
        """
        self.source_table = source_table
        self.feature_name = feature_name
        self.source_id = source_id
        self.dburl = dburl
        self.options = options

    def extract_columns(self, x):
        """Extract column and filter from a string input

        Parameters
        ----------
        x: str
            The column and filter pair in the form :code:`column:filter`

        Returns
        -------
        (str, str)
            The extracted column and filter pair
        """
        return x.split(":") if len(x.split(":")) == 2 else ("fclass", x)

    def get_core(self, dburl):
        """Instantiates an appropriate core based on given database url

        Parameters
        ----------
        dburl : str
            Database url used to configure backend connection

        Returns
        -------
        core : :code:`geomancer.backend.cores.DBCore`
            DBCore instance to access DB-specific methods
        """
        name = make_url(dburl).get_backend_name()
        Core = CORES[name]
        return Core(dburl, self.options)

    @abc.abstractmethod
    def query(self, source, target, core, column):
        """Build the query used to extract features

        Parameters
        ----------
        source : :class:`sqlalchemy.schema.Table`
            Source table to extract features from.
        target : :class:`sqlalchemy.schema.Table`
            Target table to add features to.
        core : :class:`geomancer.backend.cores.base.DBCore`
            DBCore instance to access DB-specific methods
        column : string
            Column to look the geometries from. The default is :code:`WKT`

        Returns
        -------
        :class:`sqlalchemy.sql.expression.ClauseElement`
            The statement to query features with.

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError

    def _include_column(self, col, keep_index, features_only):
        if features_only:
            return col.key in ("__index_level_0__", self.feature_name)
        if keep_index:
            return True
        return col.key != "__index_level_0__"

    @logger.catch(reraise=True)
    def cast(
        self,
        df,
        dburl=None,
        column="WKT",
        keep_index=False,
        features_only=False,
    ):
        """Apply the feature transform to an input :class:`pandas.DataFrame`

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`WKT` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.
        dburl : str, optional
            Database url used to configure backend connection
        column : str, optional
            Column to look the geometries from. The default is :code:`WKT`
        keep_index : boolean, optional
            Include index in output dataframe
        features_only : boolean, optional
            Only return features as output dataframe. Automatically sets
            :code:`keep_index` to :code:`True`.

        Returns
        -------
        :class:`pandas.DataFrame`
            Output dataframe with the features per given point
        """
        dburl = dburl or self.dburl
        if not dburl:
            raise ValueError("dburl was not supplied")

        if features_only:
            keep_index = True

        core = self.get_core(dburl)

        # Get engine
        engine = core.get_engine()

        # Get source and target tables
        source, target = core.get_tables(
            source_uri=self.source_table, target_df=df, engine=engine
        )

        # Build query
        query = self.query(source, target, core, column)

        # Filter output columns
        query = select(
            [
                col
                for col in query.columns
                if self._include_column(col, keep_index, features_only)
            ]
        ).select_from(query)

        # Perform query
        results = engine.execute(query)

        return pd.DataFrame(list(results), columns=results.keys())
