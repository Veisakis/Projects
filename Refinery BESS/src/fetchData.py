import os
import sys
import requests
import numpy as np
import pandas as pd

import config


def from_trading(prices_raw, year):
    prices_year = prices_raw[prices_raw['Year'] == year]
    prices = prices_year['price_new'].iloc[::24]
    prices = prices.to_frame().rename(columns={'price_new': 0}).reset_index().drop(columns="index")

    for i in range(1, 24):
        filtered = prices_year['price_new'].iloc[i::24]
        df_newcol = pd.DataFrame(filtered)
        df_newcol = df_newcol.reset_index().drop(columns="index")
        prices[i] = df_newcol

    prices.columns = range(1,25)
    return prices


def to_series(frame):
    return frame.stack().reset_index(drop=True)
