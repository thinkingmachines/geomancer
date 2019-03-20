# -*- coding: utf-8 -*-

# Import modules
import pytest
from tests.backend.cores.base_test_dbcore import BaseTestDBCore

# Import from package
from geomancer.backend.cores.sqlite import SQLiteCore


class TestSQLiteCore(BaseTestDBCore):
    @pytest.fixture
    def core(self):
        return SQLiteCore("sqlite:///tests/data/source.sqlite")

    @pytest.fixture
    def name(self):
        return "sqlite"

    @pytest.fixture(params=["gis_osm_pois_free_1", "gis_osm_roads_free_1"])
    def test_tables(self, request):
        return request.param
