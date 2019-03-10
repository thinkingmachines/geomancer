# -*- coding: utf-8 -*-

# Import modules
import pytest

# Import from package
from geomancer import BQConfig, SQLiteConfig


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


@pytest.fixture
def table_path():
    """Return path to SQLite table"""
    return "tests/data/source.sqlite"
