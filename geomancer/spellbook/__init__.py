# -*- coding: utf-8 -*-

"""
A :code:`SpellBook` is a collection of spells that can be sequentially casted
and merged in a single dataframe. This is useful if you have a feature-collection
that you want to reuse or share to other people:

    .. code-block:: python

        from geomancer.spells import DistanceToNearest, NumberOf
        from geomancer.spellbook import SpellBook
        from tests.conftest import sample_points


        # Create a spellbook
        spellbook = SpellBook(
                     spells=[
                         DistanceToNearest("primary",
                                            source_table="geospatial.ph_osm.gis_osm_roads_free_1",
                                            feature_name="dist_primary"),
                         NumberOf("supermarket"
                                   source_table="geospatial.ph_osm.gis_osm_pois_free_1",
                                   feature_name="num_supermarkets"),
                     ])

SpellBooks can be distributed by exporting them to JSON files.

    .. code-block:: python

        # Export SpellBook into a file
        spellbook.author = "Juan dela Cruz"
        spellbook.description = "Good Features for Economic Indicators"
        spellbook.to_json("features_dela_cruz.json")

Now other people can easily reuse your feature extractions in with their own datasets!

    .. code-block:: python

        from geomancer.spellbook import SpellBook
        from tests.conftest import sample_points

        spellbook = SpellBook.read_json("features_dela_cruz.json")
        df = sample_points() # load your own data

        # Cast someone's Spells into your own data
        df_with_features = spellbook.cast(df)
"""

from .spellbook import SpellBook

__all__ = ["SpellBook"]
