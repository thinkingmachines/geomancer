# -*- coding: utf-8 -*-

# Import standard library
import uuid

# Import modules
import pytest
from sqlalchemy.engine.base import Engine


class BaseTestDBCore:
    """Base Test class for all DBCore implementations"""

    @pytest.fixture
    def core(self):
        raise NotImplementedError

    @pytest.fixture
    def test_tables(self):
        raise NotImplementedError

    @pytest.mark.usefixtures("core")
    def test_get_engine_return_type(self, core):
        """Test if get_engine() returns appropriate type"""
        engine = core.get_engine()
        assert isinstance(engine, Engine)

    @pytest.mark.usefixtures("core", "sample_points", "test_tables")
    def test_get_tables_source_name(self, core, sample_points, test_tables):
        """Test if source table name is the same as input"""
        engine = core.get_engine()
        source, target = core.get_tables(
            source_uri=test_tables, target_df=sample_points, engine=engine
        )
        assert test_tables == source.name

    @pytest.mark.usefixtures("core", "sample_points", "test_tables")
    def test_get_tables_target_valid_uuid(
        self, core, sample_points, test_tables
    ):
        """Test if target table name is a valid UUID v4"""
        engine = core.get_engine()
        source, target = core.get_tables(
            source_uri=test_tables, target_df=sample_points, engine=engine
        )

        def is_valid_uuid(name):
            """Validate if name is a UUID"""
            try:
                # This should work for BQ tables
                name_ = name.split(".")[-1]
                uuid_obj = uuid.UUID(name_, version=4)
            except ValueError:
                return False
            return uuid_obj.hex == name_

        assert is_valid_uuid(target.name)

    @pytest.mark.usefixtures("core", "sample_points", "test_tables")
    def test_get_tables_target_column_names(
        self, core, sample_points, test_tables
    ):
        """Test if target column names is as expected"""
        engine = core.get_engine()
        source, target = core.get_tables(
            source_uri=test_tables, target_df=sample_points, engine=engine
        )
        expected = sample_points.columns.to_list()
        assert set(expected).issubset(
            set([col.name for col in target.columns])
        )

    @pytest.mark.usefixtures("core", "sample_points")
    def test_load(self, core, sample_points):
        """Test if load() method returns appropriate type"""
        target_uri = core.load(
            sample_points, **core._inspect_options(core.options)
        )
        assert isinstance(target_uri, str)

    @pytest.mark.usefixtures("core", "name")
    def test_options(self, core, name):
        """Test if default options are properly set"""
        assert core.options.name == name
