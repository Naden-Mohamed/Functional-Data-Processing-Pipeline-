import pandas as pd
from typing import Dict, Any

def remove_missing(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(axis=0, how='any')

def fill_missing(df: pd.DataFrame, fill_values: Dict[str, Any]) -> pd.DataFrame:
    return df.fillna(value=fill_values)

def auto_handle_missing(df: pd.DataFrame, strategy_num: str = "mean", strategy_cat: str = "mode") -> pd.DataFrame:
    df_clean = df.copy()
    fill_dict = {}
    for col in df_clean.columns:
        if df_clean[col].isna().sum() == 0:
            continue
        col_type = df_clean[col].dtype
        if pd.api.types.is_numeric_dtype(col_type):
            fill_value = df_clean[col].mean() if strategy_num == "mean" else df_clean[col].median()
        elif pd.api.types.is_categorical_dtype(col_type) or col_type == object:
            fill_value = df_clean[col].mode(dropna=True)[0] if not df_clean[col].mode(dropna=True).empty else "Unknown"
        elif pd.api.types.is_bool_dtype(col_type):
            fill_value = df_clean[col].mode(dropna=True)[0]
        elif pd.api.types.is_datetime64_any_dtype(col_type):
            mq = df_clean[col].mode(dropna=True)
            fill_value = mq[0] if not mq.empty else df_clean[col].dropna().min()
        else:
            fill_value = "Unknown"
        fill_dict[col] = fill_value
    return df_clean.fillna(value=fill_dict)
