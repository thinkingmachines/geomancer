# -*- coding: utf-8 -*-

"""Contains default configurations for interacting with the database engines

If you wish to override the default configurations, simply instantiate the class
and set the value you desire. For example, you wish to lengthen the expiry
date of a BigQuery table from :code:`3` hours (the default) to :code:`12` hours:

    .. code-block:: python

        from geomancer import BQConfig
        myconfig = BQConfig()
        assert myconfig.EXPIRY == 3 # Default value
        myconfig.EXPIRY = 12 # Update config
        assert myconfig.EXPIRY == 12

"""

# Import standard library
import abc


class Config(abc.ABC):
    """Base abstract configuration"""

    @abc.abstractproperty
    def name(self):
        pass


class BQConfig(Config):
    """Configuration for interacting with BigQuery

    Attributes
    ----------
    DATASET_ID : str
        Specify the BQ dataset where the input pandas.DataFrame will be loaded
        into.  Internally, we load the dataframe into a BigQuery table before
        running the actual query. Default is :code:`geomancer`.
    EXPIRY : int, None
        Number of hours for a given table to expire. Default is :code:`3`
    MAX_RETRIES : int
        Number of retries for the upload job to ensure that the table exists.
        Default is :code:`10`

    """

    @property
    def name(self):
        return "bigquery"

    DATASET_ID = "geomancer"
    EXPIRY = 3
    MAX_RETRIES = 10


class SQLiteConfig(Config):
    """Configuration for interacting with a SQLite Database

    Attributes
    ----------
    INDEX : bool
        Write pandas.DataFrame index as column. Uses INDEX_LABEL for column name
        Default is :code:`False`
    INDEX_LABEL : str or None
        Column label for the index columns
        Default is :code:`None`
    IF_EXISTS : str
        How to behave if the table already exists. Default is
        :code:`replace` (drop the table before inserting new values).
        Other options are :code:`fail` (raise a ValueError) and
        :code:`append` (insert new values to the existing table)
    """

    @property
    def name(self):
        return "sqlite"

    INDEX = False
    INDEX_LABEL = None
    IF_EXISTS = "replace"
