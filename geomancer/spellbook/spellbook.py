# -*- coding: utf-8 -*-


# Import standard library
import importlib
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
        df : :class:`pandas.DataFrame`
            Dataframe containing the points to compare upon. By default, we
            will look into the :code:`geometry` column. You can specify your
            own column by passing an argument to the :code:`column` parameter.

        Returns
        -------
        :class:`pandas.DataFrame`
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
                {
                    **s.__dict__,
                    "module": type(s).__module__,
                    "type": type(s).__name__,
                }
                for s in self.spells
            ],
        }
        if filename:
            with open(filename, "w") as f:
                json.dump(obj, f, **kwargs)
        else:
            return json.dumps(obj, **kwargs)

    @classmethod
    def _instantiate_spells(cls, spells):
        for spell in spells:
            mod = importlib.import_module(spell.pop("module"))
            spell_cls = getattr(mod, spell.pop("type"))
            on = "{}:{}".format(
                spell.pop("source_column"), spell.pop("source_filter")
            )
            yield spell_cls(on, **spell)

    @classmethod
    def read_json(cls, filename):
        """Reads a JSON exported spell book

        Parameters
        ----------
        filename : str
            Filename of JSON file to read.

        Returns
        -------
        :class:`geomancer.spellbook.SpellBook`
            :code:`SpellBook` instance parsed from given JSON file.
        """
        with open(filename) as f:
            obj = json.load(f)
            obj["spells"] = cls._instantiate_spells(obj.pop("spells"))
            return cls(**obj)
