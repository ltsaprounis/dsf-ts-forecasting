"""Plotting utils"""
from sktime.utils.plotting import plot_series
import pandas as pd
from matplotlib import pyplot as plt
from ipywidgets import widgets
from dsf_utils.preprocessing import single_region_ts


def plot_cv_results(time_series: pd.Series, df: pd.DataFrame):
    for forecaster, eval_df in df.groupby("Forecaster"):
        plot_list = [
            eval_df["y_pred"].iloc[i].sort_index() for i in range(len(eval_df))
        ]
        plot_series(
            time_series,
            *plot_list,
            markers=["o"] + ["o" for _ in range(len(eval_df))],
        )
        plt.title(forecaster)
        plt.show()


def plot_panel_cv_results(panel_df, eval_df, region, start_date="2018-01-01"):
    start_date = pd.Period(start_date, freq="W-SUN")
    ts = panel_df[(panel_df["REGION"] == region) & (panel_df.index >= start_date)][
        "ILITOTAL"
    ]
    _eval_df = eval_df[eval_df["REGION"] == region]
    plot_list = [_eval_df["y_pred"].iloc[i].sort_index() for i in range(len(_eval_df))]
    plot_series(
        ts,
        *plot_list,
        markers=["o"] + ["o" for _ in range(len(_eval_df))],
    )
    mean_score = _eval_df["Score"].mean()
    plt.title(f"{region} - mean score across cutoffs is {mean_score: 0.2f}")
    plt.show()


def plot_interactive_panel_cv_results(panel_df, eval_df, start_date="2018-01-01"):
    regions = list(panel_df["REGION"].unique())
    _ = widgets.interact(
        plot_panel_cv_results,
        panel_df=widgets.fixed(panel_df),
        eval_df=widgets.fixed(eval_df),
        region=widgets.Dropdown(options=regions, value="California"),
        start_date=widgets.fixed(start_date),
    )


def plot_region_from_panel(panel_df, pred_df, region, start_date="2018-01-01"):
    _panel_df = panel_df.copy()
    start_date = pd.Period(start_date, freq="W-SUN")
    _panel_df = _panel_df[panel_df.index >= start_date]
    actuals = single_region_ts(_panel_df, region)
    pred = single_region_ts(pred_df, region, y_name="y_pred")
    plot_series(actuals, pred, labels=["actual", "pred"])
    plt.title(f"{region}")
    plt.show()


def plot_interactive_panel_series(panel_df, pred_df, start_date="2018-01-01"):
    regions = list(panel_df["REGION"].unique())
    _ = widgets.interact(
        plot_region_from_panel,
        panel_df=widgets.fixed(panel_df),
        pred_df=widgets.fixed(pred_df),
        region=widgets.Dropdown(options=regions, value="California"),
        start_date=widgets.fixed(start_date),
    )
