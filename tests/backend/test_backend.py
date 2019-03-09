# -*- coding: utf-8 -*-

# Import modules
import pytest
from sqlalchemy.engine.base import Engine
from sqlalchemy.schema import Table

# Import from package
from geomancer import SQLiteConfig
from geomancer.backend import get_engine, get_tables


@pytest.mark.usefixtures("sqlite_config", "table_path")
def test_get_engine_return_type(sqlite_config, table_path):
    """Check if get_engine() returns appropriate type"""
    engine = get_engine(options=sqlite_config, path=table_path)
    assert isinstance(engine, Engine)


@pytest.mark.usefixtures("sample_points", "sqlite_config", "table_path")
@pytest.mark.parametrize(
    "source_uri", ["gis_osm_pois_free_1", "gis_osm_roads_free_1"]
)
def test_get_tables_return_type(
    sample_points, sqlite_config, source_uri, table_path
):
    """Check if get_tables() returns appropriate type"""
    engine = get_engine(options=sqlite_config, path=table_path)
    source, target = get_tables(
        source_uri=source_uri,
        target_df=sample_points,
        engine=engine,
        options=sqlite_config,
        path="tests/data/source.sqlite",
    )
    assert isinstance(source, Table)
    assert isinstance(target, Table)
