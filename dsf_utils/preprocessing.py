"""Data Preprocessing Functions"""
import pandas as pd
import epiweeks as epi


def process_raw_data(
    raw_df,
    start_date="01-01-2014",
    end_date="01-01-2020",
    drop_regions=["Florida", "Commonwealth of the Northern Mariana Islands"],
):
    df = raw_df.copy()

    df["ds_wsun"] = df[["YEAR", "WEEK"]].apply(epiweeks_from_df, axis=1)
    df["ds_wsun"] = pd.to_datetime(df["ds_wsun"])
    df = df[
        (~df["REGION"].isin(drop_regions))
        & (df["ds_wsun"] >= start_date)
        & (df["ds_wsun"] <= end_date)
    ]
    return df


def epiweeks_from_df(year_week_row):
    """
    Takes an array of the form (year, week) and returns the MMWR week end-dat (Sunday)
    """
    return epi.Week(year_week_row[0], year_week_row[1]).enddate()


def single_region_ts(df, region, y_name="ILITOTAL"):
    """Get a single region

    Parameters
    ----------
    df : [type]
        [description]
    region : [type]
        [description]
    y_name : str, optional
        [description], by default "ILITOTAL"

    Returns
    -------
    [type]
        [description]
    """
    df = df.copy()
    df = df[df["REGION"] == region]
    df["ds_wsun"] = pd.PeriodIndex(df["ds_wsun"], freq="W-SUN")
    df = df.set_index("ds_wsun")
    series = df[y_name]
    series = series.sort_index()

    return series
