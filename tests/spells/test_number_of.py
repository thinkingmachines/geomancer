# -*- coding: utf-8 -*-

# Import modules
import pytest
from google.cloud import bigquery
from tests.spells.base_test_spell import BaseTestSpell, SpellHost

# Import from package
from geomancer.backend.settings import BQConfig, SQLiteConfig
from geomancer.spells import NumberOf

params = [
    SpellHost(
        spell=NumberOf(
            on="embassy",
            source_table="gis_osm_pois_free_1",
            feature_name="num_embassy",
            options=SQLiteConfig(),
        ),
        host="tests/data/source.sqlite",
    ),
    SpellHost(
        spell=NumberOf(
            on="primary",
            source_table="gis_osm_roads_free_1",
            feature_name="num_primary",
            options=SQLiteConfig(),
        ),
        host="tests/data/source.sqlite",
    ),
    pytest.param(
        SpellHost(
            spell=NumberOf(
                on="embassy",
                source_table="tm-geospatial.ph_osm.gis_osm_pois_free_1",
                feature_name="num_embassy",
                options=BQConfig(),
            ),
            host=bigquery.Client,
        ),
        marks=pytest.mark.bqtest,
    ),
    pytest.param(
        SpellHost(
            spell=NumberOf(
                on="primary",
                source_table="tm-geospatial.ph_osm.gis_osm_roads_free_1",
                feature_name="num_primary",
                options=BQConfig(),
            ),
            host=bigquery.Client,
        ),
        marks=pytest.mark.bqtest,
    ),
]


class TestNumberOf(BaseTestSpell):
    @pytest.fixture(
        params=params,
        ids=["pois-sqlite", "roads-sqlite", "pois-bq", "roads-bq"],
    )
    def spellhost(self, request):
        return request.param
