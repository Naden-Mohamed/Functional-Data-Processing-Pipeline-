# src/cleaning.py
from typing import Dict, Any
import pandas as pd

def remove_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Return a new DataFrame with any row containing NaN removed."""
    return df.dropna(axis=0, how="any").copy()


def fill_missing(df: pd.DataFrame, fill_values: Dict[str, Any]) -> pd.DataFrame:
    """Return a new DataFrame with provided per-column fill values."""
    return df.fillna(value=fill_values).copy()


def _mode_or_default(series: pd.Series, default: Any = "Unknown"):
    m = series.mode(dropna=True)
    if not m.empty:
        return m.iloc[0]
    return default


def auto_handle_missing(df: pd.DataFrame, strategy_num: str = "mean", strategy_cat: str = "mode") -> pd.DataFrame:
    """
    Return a new DataFrame where missing values are filled automatically:
    - numeric: mean or median
    - categorical/object: mode or "Unknown"
    - bool: mode
    - datetime: mode or min available date
    """
    df_clean = df.copy()
    fill_dict: Dict[str, Any] = {}

    for col in df_clean.columns:
        if df_clean[col].isna().sum() == 0:
            continue
        col_series = df_clean[col]
        dtype = col_series.dtype

        if pd.api.types.is_numeric_dtype(dtype):
            fill_value = col_series.mean() if strategy_num == "mean" else col_series.median()
        elif pd.api.types.is_bool_dtype(dtype):
            fill_value = _mode_or_default(col_series, default=False)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            m = col_series.mode(dropna=True)
            fill_value = m.iloc[0] if not m.empty else col_series.dropna().min()
        elif pd.api.types.is_categorical_dtype(dtype) or dtype == object:
            fill_value = _mode_or_default(col_series, default="Unknown")
        else:
            fill_value = "Unknown"

        fill_dict[col] = fill_value

    return df_clean.fillna(value=fill_dict).copy()
