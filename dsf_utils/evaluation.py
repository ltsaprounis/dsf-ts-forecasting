"""Evaluation Functions"""
import pandas as pd
import numpy as np
from sktime.forecasting.model_selection._split import BaseSplitter
from sktime.forecasting.model_evaluation import evaluate
from IPython.display import display


def evaluate_forecasters(
    time_series: pd.Series, cv: BaseSplitter, forecasters_dict: dict, metrics_dict: dict
) -> pd.DataFrame:
    _df_list = []
    for fcaster_name, forecaster in forecasters_dict.items():
        for metric_name, metric in metrics_dict.items():
            _ts = time_series.copy()
            _df = evaluate(
                forecaster=forecaster,
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
