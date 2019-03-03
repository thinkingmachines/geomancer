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
from loguru import logger


class Spell(abc.ABC):
    """Base class for all feature/spell implementations"""

    query = None

    @logger.catch
    @abc.abstractclassmethod
    def cast(
        cls,
        on,
        df,
        client,
        source_table,
        feature_name,
        column='geometry',
        within=10 * 1000,
        bq_load_target_id='geomancer',
        **kwargs
    ):
        """Apply the feature transform to an input pandas.DataFrame

        This is an abstract class method, and must be implemented in each subclass.

        Parameters
        ----------
        on : str
            Feature class to compare upon
        df : pandas.DataFrame
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.
        client : google.cloud.client.Client
            Cloud Client for making requests.
        source_table : str
            BigQuery table to run queries against.
        feature_name : str
            Column name for the output feature.
        column : str, optional
            Column to look the geometries from. The default is :code:`geometry`
        within : float, optional
            Look for values within a particular range. Its value is in meters,
            the default is :code:`10,000` meters.
        bq_load_target_id : str
            Specify the BQ dataset where the input pandas.DataFrame will be loaded into.
            Internally, we load the dataframe into a BigQuery table before running the actual
            query. Default is :code:`geomancer`.

        Returns
        -------
        pandas.DataFrame
            Output dataframe with the features per given point

        Raises
        ------
        NotImplementedError
            This is an abstract class method
        """
        raise NotImplementedError
