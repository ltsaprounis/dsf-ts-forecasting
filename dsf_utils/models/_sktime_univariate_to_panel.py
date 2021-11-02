"""Transform any univariate sktime forecaster to a panel-data forecaster"""
import pandas as pd


class SktimePanelForecaster:
    def __init__(
        self,
        forecaster,
        forecaster_kwargs,
        freq="W-SUN",
        ts_id_col="REGION",
        target_col="ILITOTAL",
    ):
        self.forecaster = forecaster
        self.forecaster_kwargs = forecaster_kwargs
        self.freq = freq
        self.ts_id_col = ts_id_col
        self.target_col = target_col
        self.is_fitted = False
        self.models_dict = {}

    def _process_single_ts(self, ts_df: pd.DataFrame) -> pd.Series:
        ts = ts_df[self.target_col].sort_index()
        return ts

    def fit(self, ts_df: pd.DataFrame, fh=None):
        ts_df = ts_df.copy()
        self.is_fitted = False
        for ts_name, ts in ts_df.groupby([self.ts_id_col]):
            ts = self._process_single_ts(ts)
            _forecaster = self.forecaster(**self.forecaster_kwargs)
            if _forecaster._tags["requires-fh-in-fit"]:
                _forecaster.fit(y=ts, fh=fh)
            else:
                _forecaster.fit(y=ts)
            self.models_dict[ts_name] = _forecaster

        self.is_fitted = True

    def predict(self, fh):
        pred_df = pd.DataFrame()
        for ts_name, forecaster in self.models_dict.items():
            y_pred = forecaster.predict(fh).to_frame(name="y_pred")
            y_pred[self.ts_id_col] = ts_name
            pred_df = pred_df.append(y_pred, ignore_index=False)

        return pred_df
