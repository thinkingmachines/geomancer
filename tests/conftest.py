# -*- coding: utf-8 -*-

# Import modules
import pandas as pd
import pytest


@pytest.fixture
def sample_points():
    """Return a set of POINTS in a pandas.DataFrame"""
    df = pd.read_csv("tests/data/sample_points.csv")
    return df


@pytest.fixture
def spellbook_json():
    with open("tests/data/spellbook.json") as f:
        return f.read()
