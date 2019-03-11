# -*- coding: utf-8 -*-

"""Base class for all feature or spell implementations

In Geomancer, all feature transform primitives are of the class :code:`Spell`.
When defining your own feature primitive, simply create a class that inherits
from :code:`Spell`:

    >>> from geomancer.spells.base import Spell
    >>> class MyNewFeature(Spell):
    >>>     def __init__(self):
    >>>         super(MyNewFeature, self).__init__()

All methods must be implemented in order to not raise a
:code:`NotImplementedError`.
"""

# Import standard library
import abc

# Import modules
import pandas as pd
from loguru import logger
from sqlalchemy.sql import select

from ..backend import get_tables, get_engine
from ..backend.settings import BQConfig


class Spell(abc.ABC):
    """Base class for all feature/spell implementations"""

    @abc.abstractmethod
    def __init__(self, source_table, feature_name, column="geometry"):
        """Spell constructor

        Parameters
        ----------
        source_table : str
            Table URI to run queries against.
        feature_name : str
            Column name for the output feature.
        column : str, optional
            Column to look the geometries from. The default is :code:`geometry`
        """
        self.source_table = source_table
        self.feature_name = feature_name
        self.column = column

    @abc.abstractmethod
    def query(self, source, target):
        """Build the query used to extract features

        This is an abstract method, and must be implemented in each subclass.

        Parameters
        ----------
        source : sqlalchemy.schema.Table
            Source table to extract features from.
        target : sqlalchemy.schema.Table
            Target table to add features to.

        Returns
        -------
        sqlalchemy.sql.expression.ClauseElement
            The statement to query features with.

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError

    @logger.catch
    def cast(self, df, host, options=BQConfig()):
        """Apply the feature transform to an input pandas.DataFrame

        If using BigQuery, a :code:`google.cloud.client.Client`
        must be passed in the :code:`client` parameter.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.
        host : google.cloud.client.Client or str
            Object where requests will be passed onto. If the backend database:
                * is **BigQuery**, then a :code:`google.cloud.client.Client`
                must be passed.
                * is **SQLite**, then a :code:`str` that points to the SQLite
                database must be passed.
        options : geomancer.Config
            Specify configuration for interacting with the database backend.
            Default is a BigQuery Configuration

        Returns
        -------
        pandas.DataFrame
            Output dataframe with the features per given point
        """

        # Get engine
        engine = get_engine(options, host)

        # Get source and target tables
        source, target = get_tables(
            source_uri=self.source_table,
            target_df=df,
            engine=engine,
            options=options,
            host=host,
        )

        # Build query
        query = self.query(source, target)

        # Remove temporary index column
        query = select(
            [col for col in query.columns if col.key != "__index_level_0__"]
        ).select_from(query)

        # Perform query
        results = engine.execute(query)

        return pd.DataFrame(list(results), columns=results.keys())
