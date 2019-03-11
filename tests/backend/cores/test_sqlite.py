# -*- coding: utf-8 -*-

# Import modules
import pytest
from tests.backend.cores.abc_test_dbcore import ABCTestDBCore

# Import from package
from geomancer.backend.cores.sqlite import SQLiteCore
from geomancer.backend.settings import SQLiteConfig


class TestSQLiteCore(ABCTestDBCore):
    @pytest.fixture
    def core(self):
        return SQLiteCore(host="tests/data/source.sqlite")

    @pytest.fixture
    def config(self):
        return SQLiteConfig

    @pytest.fixture(params=["gis_osm_pois_free_1", "gis_osm_roads_free_1"])
    def test_tables(self, request):
        return request.param
