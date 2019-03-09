# -*- coding: utf-8 -*-

from . import cores, settings
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table


def get_tables(source_uri, target_df, engine, options, **kwargs):
    """Create tables given a sqlalchemy.engine.base.Engine

    Parameters
    ----------
    source_uri : str
        Source table URI to run queries against.
    target_df : pandas.DataFrame
        Target table to add features to.
    engine : sqlalchemy.engine.base.Engine
        Engine with the databse dialect
    options : geomancer.Config
        Configuration for interacting with the database backend
    **kwargs
        Arguments to be passed on the DBCore constructor

    Returns
    -------
    (sqlalchemy.schema.Table, sqlalchemy.schema.Table)
        Source and Target table
    """
    if options.name == "bq":
        dbcore = cores.BigQueryCore(**kwargs)
    else:
        raise TypeError("Unknown DBCore config {}".format(type(options)))

    # Get the URI of the uploaded DataFrame
    target_uri = dbcore.load(
        df=target_df,
        dataset_id=options.DATASET_ID,
        expiry=options.EXPIRY,
        max_retries=options.MAX_RETRIES,
    )

    # Create SQLAlchemy primitives
    metadata = MetaData(bind=engine)
    source = Table(source_uri, metadata, autoload=True)
    target = Table(target_uri, metadata, autoload=True)

    return source, target


def get_engine(options, **kwargs):
    """Get the engine from the DBCore

    Parameters
    ----------
    options : geomancer.Config
        Configuration for interacting with the database backend
    **kwargs
        Arguments to be passed on the DBCore constructor

    Returns
    -------
    sqlalchemy.engine.base.Engine
    """
    if options.name == "bq":
        dbcore = cores.BigQueryCore(**kwargs)
    else:
        raise TypeError("Unknown DBCore config {}".format(type(options)))

    engine = create_engine(dbcore.database_uri)

    return engine
