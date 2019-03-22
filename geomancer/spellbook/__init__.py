# -*- coding: utf-8 -*-

"""A :code:`SpellBook` is a collection of spells that can be sequentially casted and
merged in a single dataframe
"""

# Import standard library
import json

# Import modules
import pandas as pd


class SpellBook(object):
    def __init__(self, spells, column="WKT", author=None, description=None):
        """SpellBook constructor

        Parameters
        ----------
        spells : list of :class:`geomancer.spells.Spell`
            List of spell instances.
        column : str, optional
            Column to look the geometries from. The default is :code:`WKT`
        author : str, optional
            Author of the spell book
        description : str, optional
            Description of the spell book
        """
        self.column = column
        self.spells = spells
        self.author = author
        self.description = description

    def cast(self, df):
        """Runs the cast method of each spell in the spell book

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.

        Returns
        -------
        pandas.DataFrame
            Output dataframe with the features from all spells
        """
        for spell in self.spells:
            df = df.join(
                spell.cast(
                    df, column=self.column, features_only=True
                ).set_index("__index_level_0__")
            )
        return df

    def to_json(self, filename=None, **kwargs):
        """Exports spell book as a JSON string

        Parameters
        ----------
        filename : str, optional
            Output filename. If none is given, output is returned

        Returns
        -------
        str or None
            Export of spell book in JSON format
        """
        obj = {
            **self.__dict__,
            "spells": [
                {**s.__dict__, "type": type(s).__name__} for s in self.spells
            ],
        }
        if filename:
            with open(filename, "w") as f:
                json.dump(obj, f, **kwargs)
        else:
            return json.dumps(obj, **kwargs)
