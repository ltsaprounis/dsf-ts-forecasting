"""Plotting utils"""
from sktime.utils.plotting import plot_series
import pandas as pd
from matplotlib import pyplot as plt


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
