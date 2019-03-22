# -*- coding: utf-8 -*-

"""
Spell NumberOf obtains the number of Points-of-Interests or geographic features
within a particular range. Suppose you want to find the number of supermarkets
given a set of points

.. code-block:: python

    from geomancer.spells import NumberOf
    from tests.conftest import sample_points

    # Load sample points
    df = sample_points()

    # Configure and cast the spell
    spell = NumberOf("supermarket",
                      source_table="geospatial.ph_osm.gis_osm_pois_free_1",
                      feature_name="num_supermarket")

    # Will create a new column, `num_supermarket` with the
    # appropriate features
    df_with_features = spell.cast(df, dburl="bigquery://geospatial")

"""

# Import modules
from sqlalchemy import func, distinct
from sqlalchemy.sql import select

from .base import Spell


class NumberOf(Spell):
    """Obtain the number of nearest Point-of-Interests or geographic features"""

    def __init__(self, on, within=10 * 1000, **kwargs):
        """Spell constructor

        Parameters
        ----------
        on : str
            Feature class to compare upon
        within : float, optional
            Look for values within a particular range. Its value is in meters,
            the default is :code:`10,000` meters.
        source_table : str
            Table URI to run queries against.
        feature_name : str
            Column name for the output feature.
        column : str, optional
            Column to look the geometries from. The default is :code:`WKT`
        options : :class:`geomancer.backend.settings.Config`, optional
            Specify configuration for interacting with the database backend.
            Auto-detected if not set.
        """
        super(NumberOf, self).__init__(**kwargs)
        self.source_column, self.source_filter = self.extract_columns(on)
        self.within = within

    def query(self, source, target, core, column):
        # Get all POIs of fclass `on`
        pois = select(
            [source.c[self.source_id], source.c.WKT],
            source.c[self.source_column] == self.source_filter,
        ).cte("pois")
        # Compute the distance from `column` to each POI within given distance
        distance = func.ST_Distance(
            core.ST_GeoFromText(target.c[column]),
            core.ST_GeoFromText(pois.c.WKT),
        )
        pairs = (
            select(
                [target, pois.c[self.source_id], distance.label("distance")],
                distance < self.within,
            )
            .select_from(pois)
            .cte("pairs")
        )
        # Partition results to get the smallest distance (nearest POI)
        keep_columns = [
            cols
            for cols in pairs.columns
            if cols.key not in ["distance", self.source_id]
        ]
        query = (
            select(
                [
                    *keep_columns,
                    func.count(distinct(pairs.c[self.source_id])).label(
                        self.feature_name
                    ),
                ]
            )
            .select_from(pairs)
            .group_by(*keep_columns)
        )

        return query
