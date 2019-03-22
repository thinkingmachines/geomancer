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


@pytest.fixture
def spellbook():
    return SpellBook(
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


@pytest.mark.usefixtures("spellbook", "sample_points")
def test_spellbook_spells(spellbook, sample_points):
    df = spellbook.cast(sample_points)
    assert "dist_supermarket" in df.columns
    assert "num_embassy" in df.columns


@pytest.mark.usefixtures("spellbook", "spellbook_json")
def test_spellbook_to_json(spellbook, spellbook_json):
    assert spellbook.to_json() == spellbook_json


@pytest.mark.usefixtures("spellbook", "spellbook_json")
def test_spellbook_to_json_file(spellbook, spellbook_json, tmpdir):
    filename = "spellbook.json"
    f = tmpdir.mkdir(__name__).join(filename)
    spellbook.to_json(f.strpath)
    f.read() == spellbook_json


@pytest.mark.usefixtures("spellbook", "spellbook_json")
def test_spellbook_read_json(spellbook, spellbook_json, tmpdir):
    filename = "spellbook.json"
    f = tmpdir.mkdir(__name__).join(filename)
    f.write(spellbook_json)
    _spellbook = SpellBook.read_json(f.strpath)
    assert _spellbook.column == spellbook.column
    assert _spellbook.author == spellbook.author
    assert _spellbook.description == spellbook.description
    for i, spell in enumerate(_spellbook.spells):
        assert spell.__dict__ == spellbook.spells[i].__dict__
