# -*- coding: utf-8 -*-

# Import modules
import pandas as pd
from google.cloud import bigquery
from loguru import logger

from .base import Spell
from ..common import bqutils as bq
from ..common.settings import BQConfig


class DistanceToNearest(Spell):
    """Obtain the distance to the nearest Point-of-Interest or geographic feature"""

    query = """
        WITH
            pois AS (
            SELECT
                osm_id,
                poi.WKT AS WKT
            FROM
                `{source_table}` AS poi
            WHERE
                poi.fclass = '{on}'),
            pairs AS (
            SELECT
                points.*,
                ST_DISTANCE(ST_GEOGFROMTEXT(points.{column}), pois.WKT) AS {feature_name},
                points.{column} AS points_WKT,
                points.index AS house_pkey,
                pois.WKT AS poi_WKT,
                pois.osm_id AS osm_id
            FROM
                `{table_path}` AS points,
                pois AS pois
            WHERE
                ST_DISTANCE(ST_GEOGFROMTEXT(points.{column}), pois.WKT) < {within})
        SELECT
            * EXCEPT(row_number, __index_level_0__, house_pkey, points_WKT)
        FROM (
            SELECT
                *,
                ROW_NUMBER() OVER(PARTITION BY house_pkey ORDER BY {feature_name}) AS row_number
            FROM
                pairs)
        WHERE
            row_number = 1
    """

    def __init__(self):
        super(DistanceToNearest, self).__init__()

    @classmethod
    def cast(
        cls,
        on,
        df,
        client,
        source_table,
        feature_name,
        column='geometry',
        within=10 * 1000,
        bq_options=BQConfig,
        **kwargs
    ):
        """Apply the feature transform to an input pandas.DataFrame

        Parameters
        ----------
        on : str
            Feature class to compare upon
        df : pandas.DataFrame
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.
        client : google.cloud.client.Client
            Cloud Client for making requests.
        source_table : str
            BigQuery table to run queries against.
        feature_name : str
            Column name for the output feature.
        column : str, optional
            Column to look the geometries from. The default is :code:`geometry`
        within : float, optional
            Look for values within a particular range. Its value is in meters,
            the default is :code:`10,000` meters.
        bq_options : geomancer.BQConfig
            Specify configuration for interacting with BigQuery

        Returns
        -------
        pandas.DataFrame
            Output dataframe with the features per given point
        """

        # Load dataframe into bq with expiry
        dataset = bq.fetch_bq_dataset(client, dataset_id=bq_options.DATASET_ID)
        table_path = bq.upload_df_to_bq(
            df=df,
            client=client,
            dataset=dataset,
            expiry=bq_options.EXPIRY,
            max_retries=bq_options.MAX_RETRIES,
        )

        # Format query
        q_ = cls.query.format(
            on=on,
            source_table=source_table,
            feature_name=feature_name,
            column=column,
            within=within,
            table_path=table_path,
        )
        q = ' '.join(q_.split())

        # Perform query
        logger.debug('Performing query: {}'.format(q))
        query_job = client.query(q)
        logger.info('Query job running at {}'.format(query_job.path))
        results = query_job.result()

        return results.to_dataframe()
