Features
========

Geomancer is a geospatial feature engineering library. It allows you to query
from a geospatial data warehouse in order to create features for downstream
tasks (analysis, modelling, visualization, etc.). Its features include:

- Feature primitives for geospatial feature engineering
- Ability to switch out data warehouses
- Compilation and sharing your features


Feature Primitives
------------------

The basic building blocks in Geomancer are called Spells. These are SQL queries
that were packaged in logical groups. Given a set of coordinates, you can
obtain features such as the distance to the nearest point-of-interest (POIs),
number of POIS within a certain range, and etc.

For example, we wish to obtain the distance to the nearest embassy given 
a sample of coordinates:

.. code-block:: ipython

   In [1]: # Load the sample_points as a dataframe
   In [2]: from tests.conftest import sample_points
   In [3]: df = sample_points


.. code-block:: ipython

   In  [4]: df.head()
   Out [4]:

                                 WKT  code
   0  POINT (121.0042183 14.6749145)  2082
   1  POINT (121.0052375 14.6767411)  2110
   2     POINT (121.009712 14.68067)  2082
   3  POINT (121.0093311 14.6799482)  2082
   4  POINT (121.0073296 14.6783498)  2082


The geometries are encoded as a `str` inside a column
named `WKT`. In addition, there is a `code` column that represents any
arbitrary column in your data. What Geomancer will do is just add another
column for your chosen feature while retaining the columns you originally
have.


.. code-block:: ipython

    In [5]: from geomancer.spells import DistanceToNearest

    In [6]: # Configure and cast the spell
    In [7]: spell = DistanceToNearest("embassy",
                               source_table="geospatial.ph_osm.gis_osm_pois_free_1",
                               feature_name="dist_embassy")
    In [8]: df_with_features = spell.cast(df, dburl="bigquery://geospatial")


It then returns a DataFrame with an added column, `dist_embassy`:

.. code-block:: ipython

   In  [9]: df_with_features.head()
   Out [9]:
                                 WKT  code  dist_embassy
   0  POINT (121.0042183 14.6749145)  2082   4948.580211
   1  POINT (121.0052375 14.6767411)  2110   5084.787270
   2     POINT (121.009712 14.68067)  2082   5319.746371
   3  POINT (121.0093311 14.6799482)  2082   5256.165257
   4  POINT (121.0073296 14.6783498)  2082   5162.177598


Data Warehouse Flexibility
---------------------------

Geomancer is powered by a data warehouse backend for engineering features. It is
then possible to compile features from different sources through this flexible API.
So far, we've supported (and planning to support) the following database backends:

- `Google BigQuery <https://cloud.google.com/bigquery/>`_, an analytics data warehouse from the Google Cloud Platform
- `PostGIS <https://postgis.net/>`_, a geospatial extension for PostGreSQL
- `SpatiaLite <https://www.gaia-gis.it/fossil/libspatialite/index>`_, a geospatial extension for SQLite

Most of our examples harness the power of Open Data, particularly of `Open
Street Maps <https://www.openstreetmap.org>`_. For our geographical columns we
depend on `Geofabrik's OSM data
<https://www.geofabrik.de/data/download.html>`_.

.. image:: https://storage.googleapis.com/tm-geomancer/assets/architecture.png
   :alt: Geomancer architecture

.. note::
   
   First you need to setup your data warehouse in order to accommodate
   Geomancer. For more instructions, please see the Setup instructions in this
   documentation.

Compile and share features
--------------------------

Once you've created a good set of features (or transformations), you can then compile them 
into a SpellBook and share it to others. For example, if I identified from my experiments
that the number of supermarkets and distance to primary roads are good economic indicators,
I can bind them together and share with other researchers to try on their own data.


.. code-block:: python

   from geomancer.spells import DistancetoNearest, NumberOf
   from geomancer.spellbook import SpellBook

   # Create a spellbook
   spellbook = SpellBook(
             spells=[
                 DistanceToNearest("primary",
                                    dburl="bigquery://geospatial",
                                    source_table="ph_osm.gis_osm_roads_free_1",
                                    feature_name="dist_primary"),
                 NumberOf("supermarket"
                           dburl="bigquery://geospatial",
                           source_table="geospatial.ph_osm.gis_osm_pois_free_1",
                           feature_name="num_supermarkets"),
             ])

   # Export SpellBook into a file
   spellbook.author = "Juan dela Cruz"
   spellbook.description = "Good Features for Economic Indicators"
   spellbook.to_json("features_dela_cruz.json")


You can then share this to other people so that they can cast it on their own datasets

.. code-block:: python

   from geomancer.spellbook import SpellBook
   from tests.conftest import sample_points

   spellbook = SpellBook.read_json("features_dela_cruz.json")
   df = sample_points() # load your own data
   
   # Cast someone's Spells into your own data
   df_with_features = spellbook.cast(df)
