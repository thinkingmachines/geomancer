Setup
=====

Installing the library
----------------------

Geomancer can be installed using `pip`.

.. code-block:: shell

   $ pip install geomancer

This will install **all** dependencies for every data warehouse we support.
If you wish to do this for only a specific warehouse, then you can add an
identifier.

.. code-block:: shell

   $ pip install geomancer[bq] # For BigQuery
   $ pip install geomancer[sqlite] # For SQLite
   $ pip install geomancer[psql] # For PostgreSQL (*In Progress*)

Alternatively, you can also clone the repository then run `install`.

.. code-block:: shell

   $ git clone https://github.com/thinkingmachines/geomancer.git
   $ cd geomancer
   $ python setup.py install


Setting-up your data warehouse
------------------------------

We highly-recommend using `BigQuery <https://cloud.google.com/bigquery/>`_ as
your data warehouse and `Geofabrik's OSM catalog
<https://www.geofabrik.de/data/download.html>`_ as your source of Points and
Lines of interest. 

1. First, **download a `.shp.zip` file for your Region-of-Interest (ROI)**. In this
   example we can choose the Philippines (`.shp.zip
   <https://download.geofabrik.de/asia/philippines-latest-free.shp.zip>`_) 

.. note:: 

   You can definitely choose multiple ROIs as long as you keep them in separate
   contexts. A BigQuery best practice is to put them in separate datasets. So
   if you will use Geomancer in US and in Japan, you should have two datasets
   in your project (e.g., :code:`us_osm` and :code:`jp_osm`).

2. Then, **convert all your shape files into WKT** because BigQuery accepts WKT
   files. For example, let's convert :code:`gis_osm_pois_free_1.shp` into WKT.
   You can use :code:`ogr2ogr` for this kind of task:


.. code-block:: shell

   $ ogr2ogr -f CSV gis_osm_pois_free_1.csv gis_osm_pois_free_1.shp -lco GEOMETRY=AS_WKT



You can do this for all shapefiles you currently have. At the end of this
operation, you should have a CSV file (with a WKT) column for all files.

3. **Load your files into BigQuery**. Our best practice is to just use the CSV
   filename as the table name. Refer to the `bq load instructions
   <https://cloud.google.com/bigquery/docs/bq-command-line-tool>`_ in the
   Google Cloud Platform documentation. In this example, we'll load all WKT
   files in a dataset called `ph_osm`

.. code-block:: shell

   $ bq load --source_format=CSV    \
             --skip_leading_rows=1  \
             --autodetect           \
             ph_osm.gis_osm_pois_free_1 gis_osm_pois_free_1.csv  

Geomancer assumes that your polygons are of the type :code:`STRING`. Thus, we
recommend passing the :code:`--autodetect` option when loading to BigQuery.

And that's it! When casting a spell, you can then use
:code:`bigquery://project-name` for your :code:`dburl` and
`project-name.ph_osm.gis_osm_pois_free_1` as your :code:`source_table`.

Using other data warehouses aside from BigQuery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use other data warehouses. This enables us to support SpatiaLite and
PostGIS data warehouses. In order for them to interface with Geomancer, it
should have the following characteristics:

- The column where geometries are stored should be of type :code:`STRING` and named `WKT`
- It should support GIS functions (`ST_GeomFromText`, `ST_Distance`, `ST_Length`, etc.)

Using other source datasets aside from OSM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do you have other geospatial data? Want to use Geomancer on them? It is
possible, as long as they fulfill the following requirements:

- They should have a column of geometries
- There must be a unique identifier or a primary key for each row
- There should be a way of filtering them properly 

In this way, it is then possible to query from other datasets. For example, the 
:code:`DistanceToNearest` spell accepts an argument :code:`on`. You can add a
colon :code:`:` to specify which column this spell will filter upon (default is
:code:`fclass`). For example::

   >>> DistanceToNearest("embassy", **kwargs)   # Will filter embassy in fclass (default)
   >>> DistanceToNearest("user_group:4G-users") # Will filter 4G-users in user_group 
