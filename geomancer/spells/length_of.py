# -*- coding: utf-8 -*-

"""
Spell LengthOf obtains the length of all Lines-of-Interest with a certain
radius. Suppose you want to find the length of residential roads
given a set of points:

.. code-block:: python

    from geomancer.spells import LengthOf
    from tests.conftest import sample_points

    # Load sample points
    df = sample_points()

    # Configure and cast the spell
    spell = LengthOf("residential",
                      source_table="geospatial.ph_osm.gis_osm_roads_free_1",
                      feature_name="len_residential")

    # Will create a new column, `len_residential` with the
    # appropriate features
    df_with_features = spell.cast(df, dburl="bigquery://geospatial")


.. warning::

    This spell currently doesn't work in BigQuery. In addition, the runtime for
    casting this spell is slow.

"""

# Import modules
from sqlalchemy import func
from sqlalchemy.sql import select

from .base import Spell
from ..backend.cores.bq import BigQueryCore

from loguru import logger


class LengthOf(Spell):
    """Obtain the length of all Lines-of-Interest within a certain radius"""

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
        options : :class:`geomancer.backend.settings.Config`
            Specify configuration for interacting with the database backend.
            Default is a BigQuery Configuration
        """
        super(LengthOf, self).__init__(**kwargs)
        logger.warning(
            "ST_Buffer is not yet implemented so BigQueryCore won't work: groups.google.com/d/msg/bq-gis-feedback/Yq4Ku6u2A80/ceVXU01RCgAJ"
        )
        self.source_column, self.source_filter = self.extract_columns(on)
        self.within = within

    def query(self, source, target, core, column):
        # ST_Buffer is not yet implemented so BigQueryCore won't work
        # (groups.google.com/d/msg/bq-gis-feedback/Yq4Ku6u2A80/ceVXU01RCgAJ)
        if isinstance(core, BigQueryCore):
            raise ValueError(
                "The LengthOf feature is currently incompatible with \
                BigQueryCore because ST_Buffer is not yet implemented"
            )

        # Get all lines-of-interests (LOIs) of fclass `on`
        lois = select(
            [source.c[self.source_id], source.c.WKT],
            source.c[self.source_column] == self.source_filter,
        ).cte("lois")

        # Create a buffer `within` a distance/radius around each centroid.
        # The point has to be converted to EPSG:3857 so that meters can be
        # used instead of decimal degrees for EPSG:4326.
        buff = select(
            [
                target,
                func.ST_Buffer(
                    core.ST_GeoFromText(target.c[column]), self.within
                ).label("__buffer__"),
            ]
        ).cte("buff")

        # Clip the LOIs with the buffers then calculate the length of all
        # LOIs inside each buffer.
        clip = select(
            [
                buff,
                func.ST_Intersection(
                    core.ST_GeoFromText(lois.c.WKT),
                    func.ST_Transform(buff.c["__buffer__"], 4326),
                ).label("__geom__"),
                func.ST_Length(
                    func.ST_Intersection(
                        func.ST_Transform(
                            core.ST_GeoFromText(lois.c.WKT), 3857
                        ),
                        buff.c["__buffer__"],
                    )
                ).label("__len__"),
            ],
            func.ST_Intersects(
                core.ST_GeoFromText(lois.c.WKT),
                func.ST_Transform(buff.c["__buffer__"], 4326),
            ),
        ).cte("clip")

        # Sum the length of all LOIs inside each buffer
        sum_length = (
            select(
                [
                    clip.c["__index_level_0__"],
                    func.sum(clip.c["__len__"]).label(self.feature_name),
                ]
            )
            .select_from(clip)
            .group_by(clip.c["__index_level_0__"])
            .cte("sum_length")
        )

        # Join the sum of the length of all LOIs inside each buffer
        query = select(
            [
                col
                for col in sum_length.columns
                if col.key not in ("__len__", "__geom__", "__buffer__")
            ],
            sum_length.c["__index_level_0__"] == buff.c["__index_level_0__"],
        )
        return query
