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
from sqlalchemy.engine.url import make_url
from sqlalchemy.schema import MetaData, Table

from ..settings import BQConfig, SQLiteConfig


class DBCore(abc.ABC):
    """Base class for all DBCore implementations"""

    @abc.abstractmethod
    def __init__(self, dburl, options=None):
        """Initialize the database core

        Parameters
        ----------
        dburl : str
            Database url used to configure backend connection
        options : :class:`geomancer.backend.settings.Config`, optional
            Specify configuration for interacting with the database backend.
            Auto-detected if not set.
        """
        self.dburl = make_url(dburl)
        if not options:
            options = {"bigquery": BQConfig(), "sqlite": SQLiteConfig()}[
                self.dburl.get_backend_name()
            ]
        self.options = options

    @abc.abstractmethod
    def ST_GeoFromText(self, x):
        """Custom-implementation of converting a string into a geographical type

        As it turns out, :code:`ST_GeogFromText` only exists in BigQuery and PostGIS.
        Only :code:`ST_GeomFromText` is available for Spatialite. Thus, we need to
        construct our own method for type-casting
        """
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, df):
        """Load a pandas.Dataframe into the database

        Parameters
        ----------
        df : :class:`pandas.DataFrame`
            Input dataframe

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError

    def get_tables(self, source_uri, target_df, engine):
        """Create tables given a :class:`sqlalchemy.engine.base.Engine`

        Parameters
        -----------
        source_uri : str
            Source table URI to run queries against.
        target_df : :class:`pandas.DataFrame`
            Target table to add features to.
        engine : :class:`sqlalchemy.engine.base.Engine`
            Engine with the database dialect

        Returns
        -------
        (:class:`sqlalchemy.schema.Table`, :class:`sqlalchemy.schema.Table`)
            Source and Target table
        """
        target_uri = self.load(
            df=target_df, **self._inspect_options(self.options)
        )
        # Create SQLAlchemy primitives
        metadata = MetaData(bind=engine)
        source = Table(source_uri, metadata, autoload=True)
        target = Table(target_uri, metadata, autoload=True)
        return source, target

    def get_engine(self):
        """Get the engine from the DBCore

        Returns
        -------
        :class:`sqlalchemy.engine.base.Engine`
            Engine with the database dialect
        """
        return create_engine(self.dburl)

    def _inspect_options(self, options):
        """Helper method to return the attributes of a configuration

        Returns
        -------
        dict
        """
        return dict(
            (name.lower(), getattr(options, name))
            for name in dir(options)
            if not name.startswith("__")
        )
