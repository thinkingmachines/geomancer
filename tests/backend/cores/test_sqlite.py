# -*- coding: utf-8 -*-

# Import modules
import pytest

# Import from package
from geomancer.backend.cores.sqlite import SQLiteCore


@pytest.mark.usefixtures("sqlite_config", "sample_points", "table_path")
def test_sqlitedbcore_load(sqlite_config, sample_points, table_path):
    """Test if load() method returns correct target_uri"""
    sqlite_core = SQLiteCore(host=table_path)
    target_uri = sqlite_core.load(
        df=sample_points,
        index_label=sqlite_config.INDEX_LABEL,
        index=sqlite_config.INDEX,
        if_exists=sqlite_config.IF_EXISTS,
    )
    assert isinstance(target_uri, str)
