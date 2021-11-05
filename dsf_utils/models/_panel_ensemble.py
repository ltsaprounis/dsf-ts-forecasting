"""Combine Panel Forecasters"""


class SimpleAverageCombination:
    def __init__(self, forecaster_list, ts_id_col):
        self.forecaster_list = forecaster_list
        self.ts_id_col = ts_id_col
        self.is_fitted = False

    def fit(self, train_df, fh):
        self.is_fitted = False
        for forecaster in self.forecaster_list:
            _train_df = train_df.copy()
            forecaster.fit(_train_df, fh)
        self.is_fitted = True

    def predict(self, fh):
        count = 0
        for forecaster in self.forecaster_list:
            _pred_df = (
                forecaster.predict(fh).sort_index().sort_values(by=[self.ts_id_col])
            )
            if count == 0:
                pred_df = _pred_df.copy()
            else:
                pred_df["y_pred"] = pred_df["y_pred"] + _pred_df["y_pred"]
            count += 1

        pred_df["y_pred"] = pred_df["y_pred"] / count

        return pred_df
