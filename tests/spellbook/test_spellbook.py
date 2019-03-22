# -*- coding: utf-8 -*-

# Import modules
import pandas as pd
import pytest

# Import from package
from geomancer.spellbook import SpellBook
from geomancer.spells import DistanceToNearest, NumberOf


@pytest.mark.usefixtures("sample_points")
def test_spell_dburl(sample_points):
    with pytest.raises(ValueError, match="dburl was not supplied"):
        spell = DistanceToNearest(
            on="embassy",
            source_table="gis_osm_pois_free_1",
            feature_name="dist_embassy",
        )
        spell.cast(sample_points)


@pytest.mark.usefixtures("sample_points")
def test_spell_keep_index(sample_points):
    spell = DistanceToNearest(
        on="embassy",
        source_table="gis_osm_pois_free_1",
        feature_name="dist_embassy",
    )
    df = spell.cast(
        sample_points,
        dburl="sqlite:///tests/data/source.sqlite",
        keep_index=True,
    )
    assert "__index_level_0__" in df.columns
    df = spell.cast(
        sample_points,
        dburl="sqlite:///tests/data/source.sqlite",
        keep_index=False,
    )
    assert "__index_level_0__" not in df.columns


@pytest.mark.usefixtures("sample_points")
def test_spell_features_only(sample_points):
    spell = DistanceToNearest(
        on="embassy",
        source_table="gis_osm_pois_free_1",
        feature_name="dist_embassy",
    )
    df = spell.cast(
        sample_points,
        dburl="sqlite:///tests/data/source.sqlite",
        features_only=True,
    )
    assert ["__index_level_0__", "dist_embassy"] == df.columns.tolist()


@pytest.mark.usefixtures("sample_points")
def test_spellbook_spells(sample_points):
    book = SpellBook(
        [
            DistanceToNearest(
                "supermarket",
                source_table="gis_osm_pois_free_1",
                feature_name="dist_supermarket",
                dburl="sqlite:///tests/data/source.sqlite",
            ),
            NumberOf(
                on="embassy",
                source_table="gis_osm_pois_free_1",
                feature_name="num_embassy",
                dburl="sqlite:///tests/data/source.sqlite",
            ),
        ]
    )
    df = book.cast(sample_points)
    assert "dist_supermarket" in df.columns
    assert "num_embassy" in df.columns
