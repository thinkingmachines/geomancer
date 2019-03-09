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


@pytest.fixture
def table_path():
    """Return path to SQLite table"""
    return "tests/data/source.sqlite"


@pytest.fixture
def sqlite_config():
    """Return a SQLiteConfig instance"""
    return SQLiteConfig()


@pytest.fixture
def bq_config():
    """Return a BQConfig instance"""
    return BQConfig()


@pytest.fixture
def bq_client():
    """Return a BigQuery client"""
    # TODO: Use a testing service account for this
    return bigquery.Client()
