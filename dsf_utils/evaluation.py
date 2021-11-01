"""Evaluation Functions"""
import pandas as pd
import numpy as np
from sktime.forecasting.model_evaluation import evaluate
from sktime.forecasting.model_selection import (
    CutoffSplitter,
    SlidingWindowSplitter,
    ExpandingWindowSplitter,
    SingleWindowSplitter,
)
from typing import Union
from IPython.display import display
from copy import deepcopy


def evaluate_forecasters_on_cutoffs(
    time_series: pd.Series,
    cutoffs: list,
    forecasters_dict: dict,
    metrics_dict: dict,
    fh: np.array = np.arange(3) + 1,
    window_length: int = 5 * 52,
) -> pd.DataFrame:
    _df_list = []
    for cutoff in cutoffs:
        _ts = time_series.copy()
        for fcaster_name, forecaster in forecasters_dict.items():
            for metric_name, metric in metrics_dict.items():
                _forecaster = deepcopy(forecaster)
                cv = CutoffSplitter(
                    cutoffs=np.array([cutoff]),
                    fh=fh,
                    window_length=window_length,
                )
                _df = evaluate(
                    forecaster=_forecaster,
                    y=_ts,
                    cv=cv,
                    strategy="refit",
                    return_data=True,
                    scoring=metric,
                )
                _df["Forecaster"] = fcaster_name
                _df["Metric"] = metric_name
                _df = _df.rename(columns={f"test_{metric.name}": "Score"})
                _df_list.append(_df)
    return pd.concat(_df_list)


def evaluate_forecasters(
    time_series: pd.Series,
    cv: Union[
        CutoffSplitter,
        SlidingWindowSplitter,
        ExpandingWindowSplitter,
        SingleWindowSplitter,
    ],
    forecasters_dict: dict,
    metrics_dict: dict,
) -> pd.DataFrame:
    _df_list = []
    _ts = time_series.copy()
    for fcaster_name, forecaster in forecasters_dict.items():
        for metric_name, metric in metrics_dict.items():
            _forecaster = deepcopy(forecaster)
            cv = deepcopy(cv)
            _df = evaluate(
                forecaster=_forecaster,
                y=_ts,
                cv=cv,
                strategy="refit",
                return_data=True,
                scoring=metric,
            )
            _df["Forecaster"] = fcaster_name
            _df["Metric"] = metric_name
            _df = _df.rename(columns={f"test_{metric.name}": "Score"})
            _df_list.append(_df)
    return pd.concat(_df_list)


def display_results(df, axis=0):
    results = df.groupby(["Forecaster", "Metric"], as_index=False)["Score"].mean()
    results = results.pivot(index="Forecaster", columns="Metric", values="Score")

    def highlight_min(s, props=""):
        return np.where(s == np.nanmin(s.values), props, "")

    results = results.applymap("{:,.2f}".format).style.apply(
        highlight_min, props="color:white;background-color:purple", axis=axis
    )

    display(results)
