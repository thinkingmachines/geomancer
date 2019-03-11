# -*- coding: utf-8 -*-

# Import standard library
import abc

# Import modules
import pytest
from sqlalchemy.engine.base import Engine
from sqlalchemy.schema import Table


class ABCTestDBCore(abc.ABC):
    """Base Test class for all DBCore implementations"""

    @pytest.fixture
    def core(self):
        raise NotImplementedError

    @pytest.fixture
    def config(self):
        raise NotImplementedError

    @pytest.fixture
    def test_tables(self):
        raise NotImplementedError

    @pytest.mark.usefixtures("core")
    def test_get_engine_return_type(self, core):
        """Test if get_engine() returns appropriate type"""
        engine = core.get_engine()
        assert isinstance(engine, Engine)

    @pytest.mark.usefixtures("core", "config", "sample_points", "test_tables")
    def test_get_tables_return_type(
        self, core, config, sample_points, test_tables
    ):
        """Test if get_tables() returns appropriate type"""
        engine = core.get_engine()
        source, target = core.get_tables(
            source_uri=test_tables,
            target_df=sample_points,
            engine=engine,
            options=config,
        )
        assert isinstance(source, Table)
        assert isinstance(target, Table)

    @pytest.mark.usefixtures("core", "config", "sample_points")
    def test_load(self, core, config, sample_points):
        """Test if load() method returns appropriate type"""
        target_uri = core.load(sample_points, **core._inspect_options(config))
        assert isinstance(target_uri, str)
