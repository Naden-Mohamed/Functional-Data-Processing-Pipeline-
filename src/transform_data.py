# src/transform.py
from typing import Callable, Any, Optional
import pandas as pd

def filter_rows(df: pd.DataFrame, condition: Callable[[pd.Series], bool]) -> pd.DataFrame:
    """Return a new DataFrame of rows where condition(row) is True."""
    return df[df.apply(condition, axis=1)].copy()


def add_new_column(df: pd.DataFrame, name: str, function: Callable[[pd.Series], Any]) -> pd.DataFrame:
    """Return a new DataFrame with an added column computed from rows."""
    return df.assign(**{name: df.apply(function, axis=1)}).copy()


def standardize_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return DataFrame with specified column coerced to datetime (NaT on errors)."""
    return df.assign(**{column: pd.to_datetime(df[column], errors="coerce")}).copy()


def aggregate_data(df: pd.DataFrame, group_by_col: str, agg_col: str, method: str) -> dict | None:
    """Return a dictionary of aggregated values for requested method."""
    if group_by_col not in df.columns or agg_col not in df.columns:
        return None
    grouped = df.groupby(group_by_col)[agg_col]
    if method == "sum":
        return grouped.sum().to_dict()
    if method == "mean":
        return grouped.mean().to_dict()
    if method == "count":
        return grouped.count().to_dict()
    return None


def sort_data(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """Return a new DataFrame sorted by `column`."""
    if column not in df.columns:
        return df.copy()
    return df.sort_values(by=column, ascending=ascending).reset_index(drop=True).copy()
