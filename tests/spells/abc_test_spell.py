# -*- coding: utf-8 -*-

# Import standard library
import abc

# Import modules
import pytest
from pandas import DataFrame
from sqlalchemy.sql.expression import ClauseElement

# Import from package
from geomancer import SQLiteConfig
from geomancer.backend import get_engine, get_tables


class ABCTestSpell(abc.ABC):
    """Base Test class for all spell implementations"""

    @pytest.fixture
    def spell(self):
        """Return an instance of the Spell"""
        raise NotImplementedError

    @pytest.mark.usefixtures("spell", "sample_points", "db_host_config")
    def test_query_return_type(self, spell, sample_points, db_host_config):
        """Test if query() returns the correct type"""
        host, config = db_host_config
        engine = get_engine(options=config, host=host)
        source, target = get_tables(
            source_uri=spell.source_table,
            target_df=sample_points,
            engine=engine,
            options=SQLiteConfig(),
            host=host
        )
        # Perform the test
        query = spell.query(source=source, target=target)
        assert isinstance(query, ClauseElement)

    @pytest.mark.usefixtures("spell", "sample_points", "db_host_config")
    def test_cast_return_type(self, spell, sample_points, db_host_config):
        """Test if cast() returns the correct type"""
        host, config = db_host_config
        results = spell.cast(df=sample_points, options=config, host=host)
        assert isinstance(results, DataFrame)
