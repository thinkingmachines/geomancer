.. image:: https://storage.googleapis.com/tm-geomancer/assets/header.png
      :alt: Geomancer Logo
      :align: center

Welcome to Geomancer's documentation!
=====================================

.. image:: https://img.shields.io/pypi/v/geomancer.svg?color=brightgreen&style=flat-square
        :target: https://badge.fury.io/py/geomancer
        :alt: PyPI Version

.. image:: https://img.shields.io/badge/dynamic/json.svg?color=brightgreen&label=build&query=status&url=https%3A%2F%2Fcloud.drone.io%2Fapi%2Frepos%2Fthinkingmachines%2Fgeomancer%2Fbuilds%2Flatest%3Fref%3Drefs%2Fheads%2Fmaster&style=flat-square
        :target: https://cloud.drone.io/thinkingmachines/geomancer
        :alt: Build Status

.. image:: https://img.shields.io/readthedocs/geomancer.svg?style=flat-square
        :target: https://geomancer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/coveralls/github/thinkingmachines/geomancer.svg?style=flat-square
        :target: https://geomancer.readthedocs.io/en/latest/?badge=latest
        :alt: Coverage Status

.. image:: https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square
        :target: https://opensource.org/licenses/MIT
        :alt: License: MIT


Geomancer is a geospatial feature engineering library. It leverages geospatial
data such as OpenStreetMap (OSM) alongside a data warehouse like BigQuery. You
can use this to create, share, and iterate geospatial features for your
downstream tasks (analysis, modelling, visualization, etc.).

- **Free Software**: MIT License
- **Github Repository**: https://github.com/thinkingmachines/geomancer

.. toctree::
   :maxdepth: 1
   :caption: General

   features
   setup
   usage
   changelog


.. toctree::
   :maxdepth: 1
   :caption: Developers

   contributing
   code_of_conduct

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   api/geomancer.spells.rst
   api/geomancer.spellbook.rst
   api/geomancer.backend.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
