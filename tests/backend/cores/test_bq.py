# -*- coding: utf-8 -*-

# Import modules
import pytest
from google.cloud import bigquery
from tests.backend.cores.base_test_dbcore import BaseTestDBCore

# Import from package
from geomancer.backend.cores.bq import BigQueryCore


@pytest.mark.bqtest
class TestBigQueryCore(BaseTestDBCore):
    @pytest.fixture
    def core(self):
        return BigQueryCore("bigquery://tm-geospatial")

    @pytest.fixture
    def name(self):
        return "bigquery"

    @pytest.fixture(
        params=[
            "tm-geospatial.ph_osm.gis_osm_pois_free_1",
            "tm-geospatial.ph_osm.gis_osm_roads_free_1",
        ]
    )
    def test_tables(self, request):
        return request.param
