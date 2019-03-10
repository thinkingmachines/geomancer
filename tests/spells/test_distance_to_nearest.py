# -*- coding: utf-8 -*-

import pytest
from geomancer.spells import DistanceToNearest
from tests.spells.abc_test_spell import ABCTestSpell


class TestDistanceToNearest(ABCTestSpell):
    @pytest.fixture(
        params=[
            DistanceToNearest(
                on="embassy",
                within=10 * 1000,
                source_table="gis_osm_pois_free_1",
                feature_name="dist_embassy",
                column="WKT",
            ),
            DistanceToNearest(
                on="primary",
                within=10 * 1000,
                feature_name="dist_primary",
                source_table="gis_osm_roads_free_1",
                column="WKT",
            ),
        ],
        ids=["points", "lines"],
    )
    def spell(self, request):
        """Return an instance of DistanceToNearest"""
        return request.param
