# -*- coding: utf-8 -*-

# Import modules
import pytest
from google.cloud import bigquery
from tests.backend.cores.abc_test_dbcore import ABCTestDBCore

# Import from package
from geomancer.backend.cores.bq import BigQueryCore
from geomancer.backend.settings import BQConfig


@pytest.mark.bqtest
class TestBigQueryCore(ABCTestDBCore):
    @pytest.fixture
    def core(self):
        return BigQueryCore(host=bigquery.Client())

    @pytest.fixture
    def config(self):
        return BQConfig

    @pytest.fixture(
        params=[
            "tm-geospatial.osm.gis_osm_pois_free_1",
            "tm-geospatial.osm.gis_osm_roads_free_1",
        ]
    )
    def test_tables(self, request):
        return request.param
