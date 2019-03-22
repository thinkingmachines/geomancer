# -*- coding: utf-8 -*-

"""
The Core module contains various engines that can interact with different
databases. We strive for Geomaner to be database-agnostic: a query should
ideally be executable across **all** types of data warehouse.
"""

from .bq import BigQueryCore
from .sqlite import SQLiteCore

__all__ = ["BigQueryCore", "SQLiteCore"]
