"""Utility functions used for data validation"""

import pandas as pd
from typing import Union


def ts_min_max_dates(
    dates: pd.Series,
    start_date: Union[str, pd.Timestamp],
    end_date: Union[str, pd.Timestamp],
) -> tuple:
    """Returns the min and max date of a series of dates

    Parameters
    ----------
    dates: pd.Series
        series of dates
    start_date : Union[str, pd.Timestamp]
        if not None, the function returns start date as the min date
    end_date : Union[str, pd.Timestamp]
        if not None, the function returns end_date as the max date

    Returns
    -------
    tuple
        (min_date, max_date)
    """
    if start_date is not None:
        min_date = pd.Timestamp(start_date)
    else:
        min_date = pd.Timestamp(dates.min())

    if end_date is not None:
        max_date = pd.Timestamp(end_date)
    else:
        max_date = pd.Timestamp(dates.max())

    return min_date, max_date
