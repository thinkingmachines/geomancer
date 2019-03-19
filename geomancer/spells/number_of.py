# -*- coding: utf-8 -*-

# Import modules
from sqlalchemy import func, distinct
from sqlalchemy.sql import select

from .base import Spell


class NumberOf(Spell):
    """Obtain the distance to the nearest Point-of-Interest or geographic feature"""

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
        options : geomancer.Config
            Specify configuration for interacting with the database backend.
            Default is a BigQuery Configuration
        """
        super(NumberOf, self).__init__(**kwargs)
        self.on = on
        self.within = within

    def query(self, source, target, core):
        # Get all POIs of fclass `on`
        pois = select(
            [source.c.osm_id, source.c.WKT], source.c.fclass == self.on
        ).cte("pois")
        # Compute the distance from `column` to each POI within given distance
        distance = func.ST_Distance(
            core.ST_GeoFromText(target.c[self.column]),
            core.ST_GeoFromText(pois.c.WKT),
        )
        pairs = (
            select(
                [target, pois.c.osm_id, distance.label("distance")],
                distance < self.within,
            )
            .select_from(pois)
            .cte("pairs")
        )
        # Partition results to get the smallest distance (nearest POI)
        keep_columns = [
            cols
            for cols in pairs.columns
            if cols.key not in ["distance", "osm_id"]
        ]
        query = (
            select(
                [
                    *keep_columns,
                    func.count(distinct(pairs.c.osm_id)).label(
                        self.feature_name
                    ),
                ]
            )
            .select_from(pairs)
            .group_by(*keep_columns)
        )

        return query
