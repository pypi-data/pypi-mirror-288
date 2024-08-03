#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

def clims(year_from, year_to) -> pd.DataFrame:
    """Calculate DataFrame of climate averaging periods.

    Parameters
    ----------
        year_from : int
            Year from.
        year_to : int
           Year to.

    Returns
    -------
        periods : DataFrame
            Climate averaging periods.
    """

    periods = {}
    for year in range(year_from, year_to+1):
        # Quotient and remainder for divisor=5
        a, b = divmod(year-1, 5)
        # Update when nominal range is not in the future, otherwise project
        if a*5+15 <= year_to:
            current_period = (a*5-14, a*5+15)
        periods[year] = current_period
    return pd.DataFrame(periods, index=['year_from','year_to']
                       ).T.rename_axis('year')
