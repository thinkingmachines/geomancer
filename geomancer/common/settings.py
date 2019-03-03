# -*- coding: utf-8 -*-

"""Contains default configurations for interacting with external clients

If you wish to override the default configurations, simply instantiate the class
and set the value you desire. For example, you wish to lengthen the expiry
date of a BigQuery table from 3 (the default) to 12:

    >>> from geomancer import BQConfig
    >>> myconfig = BQConfig()
    >>> assert myconfig.EXPIRY == 3 # Default value
    >>> myconfig.EXPIRY = 12 # Update config
    >>> assert myconfig.EXPIRY == 12

"""


class BQConfig:
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

    DATASET_ID = 'geomancer'
    EXPIRY = 3
    MAX_RETRIES = 10
