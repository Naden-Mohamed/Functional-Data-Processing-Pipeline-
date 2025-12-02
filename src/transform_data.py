import pandas as pd

def filter_rows(df: pd.DataFrame, condition) -> pd.DataFrame:
    """Filter rows using a boolean condition function."""
    return df[df.apply(condition, axis=1)]

def add_new_column(df: pd.DataFrame, name: str, function) -> pd.DataFrame:
    """Add a new column based on a function applied to each row."""
    return df.assign(**{name: df.apply(function, axis=1)})

def standardize_date_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Convert column to datetime (coerce errors)."""
    return df.assign(**{column: pd.to_datetime(df[column], errors='coerce')})

def aggregate_data(df: pd.DataFrame, group_by_col: str, agg_col: str, method: str):
    """Group by a column and aggregate using sum/mean/count."""
    grouped = df.groupby(group_by_col)[agg_col]
    aggregation_map = {
        "sum": grouped.sum().to_dict(),
        "mean": grouped.mean().to_dict(),
        "count": grouped.count().to_dict()
    }
    return aggregation_map.get(method)

def sort_data(df: pd.DataFrame, column: str, ascending: bool = True) -> pd.DataFrame:
    """Sort DataFrame based on a column."""
    rows = df.to_dict("records")
    sorted_rows = sorted(rows, key=lambda x: x[column], reverse=not ascending)
    return pd.DataFrame(sorted_rows)
