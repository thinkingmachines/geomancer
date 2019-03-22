# -*- coding: utf-8 -*-

# Import standard library
from collections import namedtuple

# Import modules
import pytest
from pandas import DataFrame
from sqlalchemy.sql.expression import ClauseElement

SpellDB = namedtuple("SpellDB", ["spell", "dburl"])


class BaseTestSpell:
    """Base Test class for all spell implementations"""

    @pytest.fixture
    def spelldb(self):
        """Return an instance of SpellDB

        A spelldb is simply a namedtuple with fields "spell" and "dburl." The
        first parameter consists of an initialized instance of the
        :code:`Spell`, whereas the second one is the :code:`dburl` from which
        the spell will be made.
        """
        raise NotImplementedError

    @pytest.mark.usefixtures("spelldb", "sample_points")
    def test_query_return_type(self, spelldb, sample_points):
        """Test if query() returns the correct type"""

        core = spelldb.spell.get_core(spelldb.dburl)
        engine = core.get_engine()

        source, target = core.get_tables(
            source_uri=spelldb.spell.source_table,
            target_df=sample_points,
            engine=engine,
        )
        # Perform the test
        query = spelldb.spell.query(
            source=source, target=target, core=core, column="WKT"
        )
        assert isinstance(query, ClauseElement)

    @pytest.mark.usefixtures("spelldb", "sample_points")
    def test_cast_return_type(self, spelldb, sample_points):
        """Test if cast() returns the correct type"""
        results = spelldb.spell.cast(df=sample_points, dburl=spelldb.dburl)
        assert isinstance(results, DataFrame)

    @pytest.mark.usefixtures("spelldb", "sample_points")
    def test_cast_return_not_empty(self, spelldb, sample_points):
        """Test if cast() returns a set of values. All our test cases should not be empty"""
        results = spelldb.spell.cast(df=sample_points, dburl=spelldb.dburl)
        assert results.values.size != 0

    @pytest.mark.usefixtures("spelldb")
    @pytest.mark.parametrize("on", ["fclass:embassy", "embassy"])
    def test_extract_columns_return_values(self, on, spelldb):
        """Test if extract_columns() returns a tuple (source_column, source_filter)"""
        source_column, source_filter = spelldb.spell.extract_columns(on)
        assert source_column == "fclass"
        assert source_filter == "embassy"
