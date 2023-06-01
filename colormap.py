"""
Classes and functions for keeping consistent colors
"""
import numpy as np
import colorcet as cc
import pandas as pd
from dataclasses import dataclass, field
from itertools import cycle

default_palette = np.array(cc.glasbey_dark + cc.glasbey + cc.glasbey_light)
default_palette[555] = "#888800"  # This was some obnoxiously bright yellow so I decided to tone it down
default_override = {"0.0": {6: default_palette[0]},
                    "0.1": {28: default_palette[76]},
                    "0.25": {54:cc.glasbey[0]},
                    "0.5": {388: cc.glasbey_bw[41]},
                    "celltype": {"None": "gray"}}

class ColorMap:
    # df = field(default_factory=pd.DataFrame)
    # numeric_cols = field(default_factory=list)
    # category_cols = field(default_factory=list)
    # category_maps = field(default_factory=dict)
    # palette = default_palette
    # override = default_override
    def __init__(self, df, numeric_cols, category_cols, palette=default_palette, override=default_override) -> None:
        self.numeric_cols = numeric_cols
        self.category_cols = category_cols
        self.palette = palette
        self.override = override

        # for col in self.category_cols:
        #     self.category_map
        # self.category_maps = dict(zip(self.category_cols, dict(zip(df[]))))
        self.category_maps = {col: dict(zip(df[col].unique(), cycle(self.palette))) for col in self.category_cols}

    def map(self, val, col):
        if col in self.numeric_cols:
            if val <= 0:
                default = "gray"
            else:
                default = self.palette[val % len(self.palette)]
        elif col in self.category_cols:
            default = self.category_maps.get(col, {}).get(val, "gray")
        else:
            default = "gray"
        return self.override.get(col, {}).get(val, default)
    
    def update_overrides(self, new_overrides):
        self.override.update(new_overrides)