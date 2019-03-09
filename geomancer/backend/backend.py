# -*- coding: utf-8 -*-

# Import modules
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table

from . import cores, settings

DB_CORE = {"bq": cores.BigQueryCore, "sqlite": cores.SQLiteCore}


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
    dbcore = DB_CORE[options.name](**kwargs)
    if options.name == "bq":
        target_uri = dbcore.load(
            df=target_df,
            dataset_id=options.DATASET_ID,
            expiry=options.EXPIRY,
            max_retries=options.MAX_RETRIES,
        )
    elif options.name == "sqlite":
        target_uri = dbcore.load(
            df=target_df,
            index_label=options.INDEX_LABEL,
            index=options.INDEX,
            if_exists=options.IF_EXISTS,
        )
    else:
        raise TypeError("Unknown DBCore config {}".format(type(options)))

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
    dbcore = DB_CORE[options.name](**kwargs)
    engine = create_engine(dbcore.database_uri)

    return engine
