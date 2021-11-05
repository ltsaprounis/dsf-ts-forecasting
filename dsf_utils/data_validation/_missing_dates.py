import pandas as pd
from dsf_utils.data_validation._utils import ts_min_max_dates
from typing import Union


def missing_dates(
    time_series: pd.DataFrame,
    freq: str,
    date_col: str = None,
    start_date: Union[str, pd.Timestamp] = None,
    end_date: Union[str, pd.Timestamp] = None,
) -> set:
    """Missing dates for a single time series

    Returns all the missing dates between the min and max date of a time series

    Parameters
    ----------
    time_series : pd.DataFrame
        time series, dates should have no duplicates in rows
    freq : str
        pandas time frequency
    date_col : str, optional
        column name for date column if it's None index is used, does not support
        multiindex. By default None
    start_date : Union[str, pd.Timestamp]
        if not None, the function returns missing dates starting from start_date.
        By default None
    end_date : Union[str, pd.Timestamp]
        if not None, the function returns missing dates starting from end_date.
        By default None

    Returns
    -------
    set
        missing dates of the time series
    """
    time_series = time_series.copy()
    date_series = time_series[date_col] if date_col is not None else time_series.index
    if date_series.duplicated().any():
        raise ValueError("Time series has duplicated dates")

    min_date, max_date = ts_min_max_dates(
        date_series, start_date=start_date, end_date=end_date
    )
    all_dates = pd.date_range(start=min_date, end=max_date, freq=freq)

    missing = all_dates.difference(date_series)

    return set(missing)


def panel_missing_dates(
    panel_df: pd.DataFrame,
    freq: str,
    date_col: str,
    id_cols: list,
    start_date: Union[str, pd.Timestamp] = None,
    end_date: Union[str, pd.Timestamp] = None,
) -> dict:
    """Missing dates for panel data

    Returns the missing dates between the min and max date for each of the time
    series in a panel dataframe.

    Parameters
    ----------
    panel_df : pd.DataFrame
        multiple time series
    freq : str
        pandas time frequency
    date_col : str
        column name for date column if it's None index is used, does not support
        multiindex. By default None
    id_cols : list
        list of the column names that define a single time series. For example:
            - ["store_id", "sku_id"]
            - ["store_sku_id"]
    start_date : Union[str, pd.Timestamp]
        if not None, the function returns missing dates starting from start_date.
        By default None
    end_date : Union[str, pd.Timestamp]
        if not None, the function returns missing dates starting from end_date.
        By default None

    Returns
    -------
    dict
        dictionary of the form:
            {[id_col1, id_col2, ... ]: {2020-01-01, 2020-02-07}}
    """
    panel_df = panel_df.copy()

    missing_dict = {}
    for key, ts in panel_df.groupby(id_cols, as_index=False):
        missing_set = missing_dates(
            ts, freq=freq, date_col=date_col, start_date=start_date, end_date=end_date
        )

        if len(missing_set) > 0:
            missing_dict[key] = missing_set

    return missing_dict
