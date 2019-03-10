# -*- coding: utf-8 -*-

# Import modules
import pytest
from sqlalchemy.engine.base import Engine
from sqlalchemy.schema import Table

# Import from package
from geomancer import SQLiteConfig
from geomancer.backend import get_engine, get_tables


@pytest.mark.usefixtures("db_host_config")
def test_get_engine_return_type(db_host_config):
    """Check if get_engine() returns appropriate type"""
    host, config = db_host_config
    engine = get_engine(options=config, host=host)
    assert isinstance(engine, Engine)


@pytest.mark.usefixtures("sample_points", "db_host_config")
@pytest.mark.parametrize(
    "source_uri", ["gis_osm_pois_free_1", "gis_osm_roads_free_1"]
)
def test_get_tables_return_type(sample_points, source_uri, db_host_config):
    """Check if get_tables() returns appropriate type"""
    host, config = db_host_config
    engine = get_engine(options=config, host=host)
    source, target = get_tables(
        source_uri=source_uri,
        target_df=sample_points,
        engine=engine,
        options=config,
        host=host,
    )
    assert isinstance(source, Table)
    assert isinstance(target, Table)
