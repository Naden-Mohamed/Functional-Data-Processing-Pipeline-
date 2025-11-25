# ============================================================
# TRANSFORMATION MODULE (Pure Functional Version)
# ============================================================

import pandas as pd

def filter_rows(df, condition):
   return df[df.apply(condition, axis=1)]

def add_new_column(df, name, function):
    return df.assign(**{name: df.apply(function, axis=1)}) 

def standardize_date_column(df, column):
    return df.assign(**{column: pd.to_datetime(df[column], errors='coerce')})

def aggregate_data(df, group_by_col, agg_col, method):
    grouped = df.groupby(group_by_col)[agg_col]
    aggregation_map = {
        "sum": grouped.sum().to_dict(),
        "mean": grouped.mean().to_dict(),
        "count": grouped.count().to_dict(),
    }
    return aggregation_map.get(method)
 

def sort_data(df, column, ascending=True):
    rows = df.to_dict('records')

    sorted_rows = sorted(rows, key=lambda x: x[column], reverse=not ascending)

    return pd.DataFrame(sorted_rows)

