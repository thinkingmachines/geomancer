# -*- coding: utf-8 -*-

# Import modules
import pytest
from google.cloud import bigquery
from tests.spells.base_test_spell import BaseTestSpell, SpellDB

# Import from package
from geomancer.backend.settings import SQLiteConfig
from geomancer.spells import LengthOf

params = [
    SpellDB(
        spell=LengthOf(
            on="residential",
            within=50,
            source_table="gis_osm_roads_free_1",
            feature_name="len_residential",
            options=SQLiteConfig(),
        ),
        dburl="sqlite:///tests/data/source.sqlite",
    )
]


@pytest.mark.slow
class TestLengthOf(BaseTestSpell):
    @pytest.fixture(params=params, ids=["roads-sqlite"])
    def spelldb(self, request):
        return request.param
