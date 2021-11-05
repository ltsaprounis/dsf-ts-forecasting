"""Transform any univariate sktime forecaster to a panel-data forecaster"""
import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.preprocessing import LabelEncoder


class DirectLGBMGlobalForecaster:
    def __init__(
        self,
        lgbm_kwargs=None,
        lag_window_length=12,
        calendar_features={"week": True, "year": True, "t": True},
        cat_encoder=LabelEncoder(),
        freq="W-SUN",
        ts_id_col="REGION",
        target_col="ILITOTAL",
        log_transform=True,
    ):
        self.lgbm_kwargs = lgbm_kwargs
        self.freq = freq
        self.cat_encoder = cat_encoder
        self.ts_id_col = ts_id_col
        self.target_col = target_col
        self.is_fitted = False
        self.calendar_features = calendar_features
        self.lag_window_length = lag_window_length
        self.log_transform = log_transform

    def _create_lagged_features(self, train_df):
        _train_df = train_df.copy()
        _train_df = _train_df.sort_index()
        for lag in range(1, self.lag_window_length):
            _str = f"{self.target_col}_lag{lag}"
            _train_df[_str] = _train_df.groupby([self.ts_id_col])[
                self.target_col
            ].shift(lag)
        _train_df = _train_df.dropna()
        return _train_df

    def _create_calendar_features(self, train_df, year=True, week=True, t=True):
        _train_df = train_df.copy()
        if year:
            _train_df["Year"] = _train_df.index.year
        if week:
            _train_df["Week"] = _train_df.index.week
        if t:
            min_t = np.min(_train_df.index.astype(int))
            _train_df["t"] = _train_df.index.astype(int) - min_t
        return _train_df

    def _multistep_targets(self, train_df, fh):
        _train_df = train_df.copy()
        # create a list that will store the target name for each horizon step
        targets = []
        for h_step in fh:
            _str = f"{self.target_col}_h{h_step}"
            targets.append(_str)
            _train_df[_str] = _train_df.groupby([self.ts_id_col])[
                self.target_col
            ].shift(-h_step)

        # drop original target column
        # df = df.drop(columns=target)
        # remove nas in dependent variables

        return _train_df, targets

    def _categorical_features_processing(self, train_df):
        _train_df = train_df.copy()
        _train_df[f"{self.ts_id_col}_encoded"] = self.cat_encoder.fit_transform(
            train_df[self.ts_id_col]
        )
        return _train_df

    def fit(self, ts_df: pd.DataFrame, fh):
        train_df = ts_df.copy()
        # create a model per timestep
        self.is_fitted = False
        # cat_feature_name = f"name:{self.ts_id_col}_encoded"
        if self.lgbm_kwargs is not None:
            self.models = [
                LGBMRegressor(categorical_feature=-1, **self.lgbm_kwargs)
                for _ in range(len(fh))
            ]
        else:
            self.models = [
                LGBMRegressor(categorical_feature=-1) for _ in range(len(fh))
            ]
        # feature engineering
        train_df = self._create_lagged_features(train_df)
        train_df = self._create_calendar_features(train_df, **self.calendar_features)
        train_df, targets = self._multistep_targets(train_df, fh=fh)
        train_df = self._categorical_features_processing(train_df)
        train_df = train_df.set_index("REGION", drop=True, append=True)

        # fit the models
        for h_step in range(len(fh)):
            y_name = targets[h_step]
            _train_df = train_df.copy()
            # drop rows where the target is null
            _train_df = _train_df[_train_df[y_name].notna()]
            X, y = _train_df.drop(columns=targets), _train_df[y_name]
            if self.log_transform:
                y = np.log(y + 1)
            self.models[h_step].fit(X, y)

        # create the inference dims
        self._train_max_date = train_df.index.get_level_values(0).max()
        self._pred_df = train_df[
            train_df.index.get_level_values(0) == self._train_max_date
        ].drop(columns=targets)

        self.is_fitted = True

    def predict(self, fh):
        pred_df = pd.DataFrame()
        for h_step in range(len(fh)):
            step_date = self._train_max_date + fh[h_step]
            y_pred = self.models[h_step].predict(self._pred_df)
            if self.log_transform:
                y_pred = np.exp(y_pred) - 1

            pred_df = pred_df.append(
                pd.DataFrame(
                    {
                        self.ts_id_col: self._pred_df.index.get_level_values(1),
                        "y_pred": y_pred,
                        "_date": step_date,
                    }
                ),
                ignore_index=True,
            )

        return pred_df.set_index("_date", drop=True)


class RecursiveLGBMGlobalForecaster:
    def __init__(
        self,
        lgbm_kwargs=None,
        lag_window_length=12,
        calendar_features={"week": True, "year": True, "t": True},
        cat_encoder=LabelEncoder(),
        freq="W-SUN",
        ts_id_col="REGION",
        target_col="ILITOTAL",
        log_transform=True,
    ):
        self.lgbm_kwargs = lgbm_kwargs
        self.freq = freq
        self.cat_encoder = cat_encoder
        self.ts_id_col = ts_id_col
        self.target_col = target_col
        self.is_fitted = False
        self.calendar_features = calendar_features
        self.lag_window_length = lag_window_length
        self.log_transform = log_transform

    def _create_lagged_features(self, train_df):
        _train_df = train_df.copy()
        _train_df = _train_df.sort_index()
        for lag in range(1, self.lag_window_length):
            _str = f"{self.target_col}_lag{lag}"
            _train_df[_str] = _train_df.groupby([self.ts_id_col])[
                self.target_col
            ].shift(lag)
        _train_df = _train_df.dropna()
        return _train_df

    def _create_calendar_features(self, train_df, year=True, week=True, t=True):
        _train_df = train_df.copy()
        if year:
            _train_df["Year"] = _train_df.index.year
        if week:
            _train_df["Week"] = _train_df.index.week
        if t:
            min_t = np.min(_train_df.index.astype(int))
            _train_df["t"] = _train_df.index.astype(int) - min_t
        return _train_df

    def _training_target(self, train_df):
        _train_df = train_df.copy()
        # create a list that will store the target name for each horizon step
        _str = f"{self.target_col}_h{1}"
        target = _str
        _train_df[_str] = _train_df.groupby([self.ts_id_col])[self.target_col].shift(-1)

        # drop original target column
        # df = df.drop(columns=target)
        # remove nas in dependent variables

        return _train_df, target

    def _categorical_features_processing(self, train_df):
        _train_df = train_df.copy()
        _train_df[f"{self.ts_id_col}_encoded"] = self.cat_encoder.fit_transform(
            train_df[self.ts_id_col]
        )
        return _train_df

    def _recursive_feature_update(self, pred_df, y_pred):
        pred_df_columns = list(pred_df.columns)
        _pred_df = pred_df.copy()
        old_lags = [self.target_col] + [
            f"{self.target_col}_lag{lag}"
            for lag in range(1, self.lag_window_length - 1)
        ]
        new_lags = [
            f"{self.target_col}_lag{lag}" for lag in range(1, self.lag_window_length)
        ]
        _pred_df = _pred_df.drop(columns=[old_lags[-1]])
        _pred_df = _pred_df.rename(columns=dict(zip(old_lags, new_lags)))
        _pred_df[self.target_col] = y_pred

        return _pred_df[pred_df_columns]

    def _recursive_calendar_features(
        self, pred_df, date, h_step, year=True, week=True, t=True
    ):
        _pred_df = pred_df.copy()
        if year:
            _pred_df["Year"] = date.year
        if week:
            _pred_df["Week"] = date.week
        if t:
            _pred_df["t"] = _pred_df["t"] + h_step

        return _pred_df

    def fit(self, ts_df: pd.DataFrame, fh=None):
        train_df = ts_df.copy()
        # create a model per timestep
        self.is_fitted = False
        if self.lgbm_kwargs is None:
            self.model = LGBMRegressor(categorical_feature=-1)
        else:
            self.model = LGBMRegressor(categorical_feature=-1, **self.lgbm_kwargs)
        # feature engineering
        train_df = self._create_lagged_features(train_df)
        train_df = self._create_calendar_features(train_df, **self.calendar_features)
        train_df, target = self._training_target(train_df)
        train_df = self._categorical_features_processing(train_df)
        train_df = train_df.set_index("REGION", drop=True, append=True)

        _train_df = train_df.copy()
        # drop rows where the target is null
        _train_df = _train_df[_train_df[target].notna()]
        X, y = _train_df.drop(columns=target), _train_df[target]
        if self.log_transform:
            y = np.log(y + 1)
        self.model.fit(X, y)

        # create the inference dims
        self._train_max_date = train_df.index.get_level_values(0).max()
        self._pred_df = train_df[
            train_df.index.get_level_values(0) == self._train_max_date
        ].drop(columns=[target])

        self.is_fitted = True

    def predict(self, fh):
        pred_df = pd.DataFrame()
        _rec_pred_df = self._pred_df.copy()
        _pred_columns = list(self._pred_df.columns)
        for h_step in range(len(fh)):
            step_date = self._train_max_date + fh[h_step]
            y_pred = self.model.predict(_rec_pred_df)

            if self.log_transform:
                y_pred = np.exp(y_pred) - 1

            pred_df = pred_df.append(
                pd.DataFrame(
                    {
                        self.ts_id_col: self._pred_df.index.get_level_values(1),
                        "y_pred": y_pred,
                        "_date": step_date,
                    }
                ),
                ignore_index=True,
            )

            # update pred_df
            _rec_pred_df = self._recursive_feature_update(_rec_pred_df, y_pred)
            _rec_pred_df = self._recursive_calendar_features(
                _rec_pred_df, step_date, fh[h_step], **self.calendar_features
            )
            _rec_pred_df = _rec_pred_df[_pred_columns]

        return pred_df.set_index("_date", drop=True)
