Usage
=====

All of the feature engineering functions in Geomancer are called "spells". For
example, you want to get the distance to the nearest supermarket for each
point.

.. code-block:: python

    from geomancer.spells import DistanceToNearest

    # Load the dataset in a pandas dataframe
    # df = load_dataset()

    dist_spell = DistanceToNearest(
        "supermarket",
        source_table="ph_osm.gis_osm_pois_free_1",
        feature_name="dist_supermarket",
    ).cast(df, dburl="bigquery://project-name")

Compose multiple spells into a "spell book" which you can export as a JSON file.

.. code-block:: python

    from geomancer.spells import DistanceToNearest
    from geomancer.spellbook import SpellBook

    spellbook = SpellBook([
        DistanceToNearest(
            "supermarket",
            source_table="ph_osm.gis_osm_pois_free_1",
            feature_name="dist_supermarket",
            dburl="bigquery://project-name",
        ),
        DistanceToNearest(
            "embassy",
            source_table="ph_osm.gis_osm_pois_free_1",
            feature_name="dist_embassy",
            dburl="bigquery://project-name",
        ),
    ])
    spellbook.to_json("dist_supermarket_and_embassy.json")

You can share the generated file so other people can re-use your feature extractions
with their own datasets.

.. code-block:: python

    from geomancer.spellbook import SpellBook

    # Load the dataset in a pandas dataframe
    # df = load_dataset()

    spellbook = SpellBook.read_json("dist_supermarket_and_embassy.json")
    dist_supermarket_and_embassy = spellbook.cast(df)
