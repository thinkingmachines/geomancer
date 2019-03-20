# -*- coding: utf-8 -*-

"""Base class for all DBCore implementations

A DBCore is simply a database backend. It can be BigQuery, PostGIS, or an
SQLite database. Whenever you want to add a new DBCore, simply
subclass from the base :code:`DBCore` class and implement the required methods
"""

# Import standard library
import abc

# Import modules
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table


class DBCore(abc.ABC):
    """Base class for all DBCore implementations"""

    @abc.abstractmethod
    def __init__(self, dburl):
        """Initialize the database core

        Parameters
        ----------
        dburl : str
            Database url used to configure backend connection
        """
        self.dburl = dburl

    @abc.abstractmethod
    def ST_GeoFromText(self, x):
        """Custom-implementation of the GeoFromTextm method

        This is an abstract method, and must be implemented in each subclass.

        As it turns out, ST_GeogFromText only exists in BigQuery and PostGIS.
        Only ST_GeomFromText is available for Spatialite. Thus, we need to
        construct our own GeoFromText method for type-casting
        """
        raise NotImplementedError

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

    def get_tables(self, source_uri, target_df, engine, options):
        """Create tables given a sqlalchemy.engine.base.Engine

        Parameters
        -----------
        source_uri : str
            Source table URI to run queries against.
        target_df : pandas.DataFrame
            Target table to add features to.
        engine : sqlalchemy.engine.base.Engine
            Engine with the databse dialect
        options : geomancer.Config
            Configuration for interacting with the database backend

        Returns
        -------
        (sqlalchemy.schema.Table, sqlalchemy.schema.Table)
            Source and Target table
        """
        target_uri = self.load(df=target_df, **self._inspect_options(options))
        # Create SQLAlchemy primitives
        metadata = MetaData(bind=engine)
        source = Table(source_uri, metadata, autoload=True)
        target = Table(target_uri, metadata, autoload=True)
        return source, target

    def get_engine(self):
        """Get the engine from the DBCore"""
        return create_engine(self.dburl)

    def _inspect_options(self, options):
        """Helper method to return the attribues of a Config"""
        return dict(
            (name.lower(), getattr(options, name))
            for name in dir(options)
            if not name.startswith("__")
        )
