# -*- coding: utf-8 -*-

"""Common utility functions for interacting with BigQuery"""

# Import standard library
import uuid
import time
import datetime
import pytz

# Import modules
from google.cloud import bigquery
from google.api_core.exceptions import Conflict
from loguru import logger


def upload_df_to_bq(df, client, dataset, expiry=3, max_retries=10):
    """Upload a pandas.Dataframe as a BigQuery table with a unique 32-char ID

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe to upload to BigQuery
    client : google.cloud.client.Client
        Cloud Client for making requests
    dataset : google.cloud.bigquery.dataset.Dataset
        Dataset to upload the DataFrame into
    expiry : int, None
        Number of hours for a given table to expire. Default
        is :code:`3`.
    max_retries: int
        Number of retries for the upload job to ensure
        that the table exists. Default is :code:`10`

    Returns
    -------
    str
        The full path for the created table
    """
    # Generate a unique table_id for every dataframe upload job
    table_id = uuid.uuid4().hex
    table_ref = dataset.table(table_id)

    # Run job
    df = df.reset_index()
    job = client.load_table_from_dataframe(df, table_ref)

    # Create full table path
    table_path = '{}.{}.{}'.format(
        dataset.project, dataset.dataset_id, table_id
    )

    # Poll until the job is complete
    while max_retries > 0 and not job.done():
        logger.debug(
            'Upload job is not yet done, retrying... (Retries left: {})'.format(
                max_retries
            )
        )
        max_retries -= 1
        time.sleep(10)
        job.reload()

    logger.debug('Done uploading dataframe to: {}'.format(table_path))

    # Wait for the table to be uploaded before setting expiry
    if expiry:
        set_table_expiry(client, table_ref, expiry)

    return table_path


def set_table_expiry(client, table_ref, expiry):
    """Set expiration date of table in hours

    Parameters
    ----------
    client : google.cloud.client.Client
        Cloud Client for making requests
    table_ref : google.cloud.bigquery.table.TableReference
        Reference to a BigQuery table
    expiry : int
        Expiration in hours
    """
    table = client.get_table(table_ref)
    expiration = datetime.datetime.now(pytz.utc) + datetime.timedelta(
        hours=expiry
    )
    table.expires = expiration
    client.update_table(table, ['expires'])
    logger.debug('Table will expire in {} hour/s'.format(expiry))


def fetch_bq_dataset(client, dataset_id):
    """Fetch a BigQuery Dataset if it exists, else, create a new one

    Parameters
    ----------
    client : google.cloud.client.Client
        Cloud Client for making requests
    dataset_id : str
        ID to name the created Dataset

    Returns
    -------
    google.cloud.bigquery.dataset.Dataset
        The Dataset class to build tables from
    """
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    try:
        dataset = client.create_dataset(dataset)
    except Conflict:
        dataset = client.get_dataset(dataset_ref)

    return dataset
