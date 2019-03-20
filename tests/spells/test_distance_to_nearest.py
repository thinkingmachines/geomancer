# -*- coding: utf-8 -*-

# Import modules
import pytest
from tests.spells.base_test_spell import BaseTestSpell, SpellDB

# Import from package
from geomancer.backend.settings import BQConfig, SQLiteConfig
from geomancer.spells import DistanceToNearest

params = [
    SpellDB(
        spell=DistanceToNearest(
            on="embassy",
            source_table="gis_osm_pois_free_1",
            feature_name="dist_embassy",
            options=SQLiteConfig(),
        ),
        dburl="sqlite:///tests/data/source.sqlite",
    ),
    SpellDB(
        spell=DistanceToNearest(
            on="primary",
            source_table="gis_osm_roads_free_1",
            feature_name="dist_primary",
            options=SQLiteConfig(),
        ),
        dburl="sqlite:///tests/data/source.sqlite",
    ),
    pytest.param(
        SpellDB(
            spell=DistanceToNearest(
                on="embassy",
                source_table="tm-geospatial.ph_osm.gis_osm_pois_free_1",
                feature_name="dist_embassy",
                options=BQConfig(),
            ),
            dburl="bigquery://tm-geospatial",
        ),
        marks=pytest.mark.bqtest,
    ),
    pytest.param(
        SpellDB(
            spell=DistanceToNearest(
                on="primary",
                source_table="tm-geospatial.ph_osm.gis_osm_roads_free_1",
                feature_name="dist_primary",
                options=BQConfig(),
            ),
            dburl="bigquery://tm-geospatial",
        ),
        marks=pytest.mark.bqtest,
    ),
]


class TestDistanceToNearest(BaseTestSpell):
    @pytest.fixture(
        params=params,
        ids=["pois-sqlite", "roads-sqlite", "pois-bq", "roads-bq"],
    )
    def spelldb(self, request):
        return request.param
