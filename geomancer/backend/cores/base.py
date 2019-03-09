# -*- coding: utf-8 -*-

"""Base class for all DBCore implementations

A DBCore is simply a database backend. It can be BigQuery, PostGIS, or an
SQLite database. Whenever you want to add a new DBCore, simply
subclass from the base :code:`DBCore` class and implement the required methods
"""

# Import standard library
import abc


class DBCore(abc.ABC):
    """Base class for all DBCore implementations"""

    @abc.abstractmethod
    def load(self, df):
        """Load a pandas.Dataframe into the Database

        This is an abstract method, and must be implemented in each subclass.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError
