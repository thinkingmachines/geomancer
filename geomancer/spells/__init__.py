# -*- coding: utf-8 -*-

"""
Spells are primitives that you can use for engineering features. They are
first instantiated, and then casted on a DataFrame of points.
"""

from .distance_to_nearest import DistanceToNearest
from .number_of import NumberOf
from .length_of import LengthOf

__all__ = ["DistanceToNearest", "NumberOf", "LengthOf"]
