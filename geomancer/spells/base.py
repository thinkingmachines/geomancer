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
from sqlalchemy import literal_column
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql import select

from ..common import bqutils as bq
from ..common.settings import BQConfig


class Spell(abc.ABC):
    """Base class for all feature/spell implementations"""

    @abc.abstractmethod
    def __init__(self, source_table, feature_name, column='geometry'):
        """Spell constructor

        Parameters
        ----------
        source_table : str
            BigQuery table to run queries against.
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

        This is an abstract class method, and must be implemented in each subclass.

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
            This is an abstract class method
        """
        raise NotImplementedError

    @logger.catch
    def cast(self, df, client, bq_options=BQConfig, **kwargs):
        """Apply the feature transform to an input pandas.DataFrame

        This is an abstract class method, and must be implemented in each subclass.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.
        client : google.cloud.client.Client
            Cloud Client for making requests.
        bq_options : geomancer.BQConfig
            Specify configuration for interacting with BigQuery

        Returns
        -------
        pandas.DataFrame
            Output dataframe with the features per given point
        """
        # Load dataframe into bq with expiry
        dataset = bq.fetch_bq_dataset(client, dataset_id=bq_options.DATASET_ID)
        table_path = bq.upload_df_to_bq(
            df=df,
            client=client,
            dataset=dataset,
            expiry=bq_options.EXPIRY,
            max_retries=bq_options.MAX_RETRIES,
        )

        # Retrieve table metadata
        database_url = "bigquery://{}".format(client.project)
        engine = create_engine(database_url)
        metadata = MetaData(bind=engine)
        source = Table(self.source_table, metadata, autoload=True)
        target = Table(table_path, metadata, autoload=True)

        # Build query
        query = self.query(source, target)

        # Remove temporary index column
        query = select(
            [literal_column("* EXCEPT (__index_level_0__)")]
        ).select_from(query)

        # Perform query
        results = engine.execute(query)

        return pd.DataFrame(list(results), columns=results.keys())
