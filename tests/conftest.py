# -*- coding: utf-8 -*-

# Import modules
import pandas as pd
import pytest
from google.cloud import bigquery

# Import from package
from geomancer import BQConfig, SQLiteConfig


@pytest.fixture
def sample_points():
    """Return a set of POINTS in a pandas.DataFrame"""
    df = pd.read_csv("tests/data/sample_points.csv")
    return df


@pytest.fixture(
    params=[
        ("tests/data/source.sqlite", SQLiteConfig()),
        pytest.param(
            (bigquery.Client(), BQConfig()), marks=pytest.mark.bqtest
        ),
    ],
    ids=["sqlite", "bq"],
)
def db_host_config(request):
    """Return a (host, Config) tuple"""
    return request.param
