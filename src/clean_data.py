import pandas as pd

# ================================
# Cleaning Data (Pure Functional)
# ================================

def get_fill_value(series: pd.Series, strategy_num="mean", strategy_cat="mode"):
    """
    Determine fill value based on column type.
    Numeric: mean or median
    Categorical: mode or "Unknown"
    Bool: mode
    Datetime: mode or min
    """
    if pd.api.types.is_numeric_dtype(series):
        return series.mean() if strategy_num == "mean" else series.median()
    if pd.api.types.is_categorical_dtype(series) or series.dtype == object:
        mode = series.mode(dropna=True)
        return mode[0] if not mode.empty else "Unknown"
    if pd.api.types.is_bool_dtype(series):
        mode = series.mode(dropna=True)
        return mode[0] if not mode.empty else False
    if pd.api.types.is_datetime64_any_dtype(series):
        mode = series.mode(dropna=True)
        return mode[0] if not mode.empty else series.dropna().min()
    return "Unknown"

def auto_handle_missing(df: pd.DataFrame, strategy_num="mean", strategy_cat="mode") -> pd.DataFrame:
    """
    Pure function: fill missing values for all columns using get_fill_value.
    Returns new DataFrame.
    """
    return df.apply(lambda col: col.fillna(get_fill_value(col, strategy_num, strategy_cat)) 
                    if col.isna().any() else col)
