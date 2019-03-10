# -*- coding: utf-8 -*-

# Import modules
import pytest

# Import from package
from geomancer.backend.cores.base import DBCore


@pytest.mark.usefixtures("sample_points")
def test_load_abstract(sample_points):
    with pytest.raises(TypeError):

        class DummyCore(DBCore):
            pass

        DummyCore(host=":memory:")
