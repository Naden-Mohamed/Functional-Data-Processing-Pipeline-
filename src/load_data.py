import pandas as pd
import sqlite3
from typing import Callable

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_json(path: str) -> pd.DataFrame:
    return pd.read_json(path)

def load_sql(db_path: str, query: str = "SELECT * FROM sales") -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

LOADERS = {
    'csv': load_csv,
    'json': load_json,
    'sql': load_sql,
}

def load_data(source_type: str, source: str, query: str | None = None) -> pd.DataFrame:
    loader: Callable = LOADERS.get(source_type.lower(), lambda x: pd.DataFrame())
    
    if source_type.lower() == 'sql' and query:
        return loader(source, query)
    else:
        return loader(source)

