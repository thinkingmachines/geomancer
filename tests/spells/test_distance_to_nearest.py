# -*- coding: utf-8 -*-

# Import modules
import pytest
from google.cloud import bigquery
from tests.spells.base_test_spell import BaseTestSpell, SpellHost

# Import from package
from geomancer.backend.settings import BQConfig, SQLiteConfig
from geomancer.spells import DistanceToNearest

params = [
    SpellHost(
        spell=DistanceToNearest(
            on="embassy",
            source_table="gis_osm_pois_free_1",
            feature_name="dist_embassy",
            options=SQLiteConfig(),
        ),
        host="tests/data/source.sqlite",
    ),
    SpellHost(
        spell=DistanceToNearest(
            on="primary",
            source_table="gis_osm_roads_free_1",
            feature_name="dist_primary",
            options=SQLiteConfig(),
        ),
        host="tests/data/source.sqlite",
    ),
    pytest.param(
        SpellHost(
            spell=DistanceToNearest(
                on="embassy",
                source_table="tm-geospatial.osm.gis_osm_pois_free_1",
                feature_name="dist_embassy",
                options=BQConfig(),
            ),
            host=bigquery.Client(),
        ),
        marks=pytest.mark.bqtest,
    ),
    pytest.param(
        SpellHost(
            spell=DistanceToNearest(
                on="primary",
                source_table="tm-geospatial.osm.gis_osm_roads_free_1",
                feature_name="dist_primary",
                options=BQConfig(),
            ),
            host=bigquery.Client(),
        ),
        marks=pytest.mark.bqtest,
    ),
]


class TestDistanceToNearest(BaseTestSpell):
    @pytest.fixture(
        params=params,
        ids=["pois-sqlite", "roads-sqlite", "pois-bq", "roads-bq"],
    )
    def spellhost(self, request):
        return request.param
