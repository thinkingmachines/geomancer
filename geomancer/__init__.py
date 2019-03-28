# -*- coding: utf-8 -*-

"""Geomancer"""

import os
from .backend.settings import BQConfig, SQLiteConfig

os.environ["LOGURU_LEVEL"] = "INFO"

__version__ = "1.0.0"
__author__ = "Thinking Machines Data Science"
__email__ = "hello@thinkingmachin.es"

__all__ = ["BQConfig", "SQLiteConfig"]
