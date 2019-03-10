# -*- coding: utf-8 -*-

# Import modules
import pytest

# Import from package
from geomancer.backend.cores.bq import BigQueryCore


@pytest.mark.bqtest
@pytest.mark.usefixtures("sample_points", "bq_config", "bq_client")
def test_bqdbcore_load(sample_points, bq_config, bq_client):
    """Test if load() method returns correct target_uri"""
    bq_core = BigQueryCore(host=bq_client)
    target_uri = bq_core.load(
        df=sample_points,
        dataset_id=bq_config.DATASET_ID,
        expiry=bq_config.EXPIRY,
        max_retries=bq_config.MAX_RETRIES,
    )
    assert isinstance(target_uri, str)
    assert target_uri == "{}.{}.{}".format(
        bq_client.project, bq_config.DATASET_ID, target_uri.split(".")[2]
    )
