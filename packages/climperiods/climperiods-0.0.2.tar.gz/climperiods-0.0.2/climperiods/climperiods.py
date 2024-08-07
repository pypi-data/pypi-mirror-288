#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
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

     # All years this function is likely to be run for (can be extended)
    all_years = np.arange(1800, 2101, dtype=int)

    # Select year range required and integer divide by 5 to chunk
    years = pd.Index(np.arange(year_from, year_to+1, dtype=int), name='years')
    chunks = (all_years-1)//5

    # Calculate 30-year windows then filter out future years and forward fill
    periods_all = pd.DataFrame({'year_from': chunks*5-14,
                                'year_to': chunks*5+15}, index=all_years)
    periods = periods_all.where(periods_all['year_to']<=year_to
                               ).ffill().astype(int).reindex(years)
    return periods
