# -*- coding: utf-8 -*-

# Import standard library
from collections import namedtuple

# Import modules
import pytest
from pandas import DataFrame
from sqlalchemy.sql.expression import ClauseElement

SpellHost = namedtuple("SpellHost", ["spell", "host"])


class BaseTestSpell:
    """Base Test class for all spell implementations"""

    @pytest.fixture
    def spellhost(self):
        """Return an instance of SpellHost

        A spellhost is simply a namedtuple with fields "spell" and "host." The
        first parameter consists of an initialized instance of the
        :code:`Spell`, whereas the second one is the :code:`host` from which
        the spell will be made.
        """
        raise NotImplementedError

    def instantiate_host(self, host):
        """Filter method to instantiate a BigQuery host"""
        try:
            h = host()
        except TypeError:
            h = host
        return h

    @pytest.mark.usefixtures("spellhost", "sample_points")
    def test_query_return_type(self, spellhost, sample_points):
        """Test if query() returns the correct type"""

        core = spellhost.spell.core(host=self.instantiate_host(spellhost.host))
        engine = core.get_engine()

        source, target = core.get_tables(
            source_uri=spellhost.spell.source_table,
            target_df=sample_points,
            engine=engine,
            options=spellhost.spell.options,
        )
        # Perform the test
        query = spellhost.spell.query(source=source, target=target, core=core)
        assert isinstance(query, ClauseElement)

    @pytest.mark.usefixtures("spellhost", "sample_points")
    def test_cast_return_type(self, spellhost, sample_points):
        """Test if cast() returns the correct type"""
        results = spellhost.spell.cast(
            df=sample_points, host=self.instantiate_host(spellhost.host)
        )
        assert isinstance(results, DataFrame)

    @pytest.mark.usefixtures("spellhost", "sample_points")
    def test_cast_return_not_empty(self, spellhost, sample_points):
        """Test if cast() returns a set of values. All our test cases should not be empty"""
        results = spellhost.spell.cast(
            df=sample_points, host=self.instantiate_host(spellhost.host)
        )
        assert results.values.size != 0
