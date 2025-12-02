# src/load_data.py
from typing import Callable, Optional
import pandas as pd
import sqlite3

def load_csv(path: str) -> pd.DataFrame:
    """Pure-ish loader: returns DataFrame (may raise on bad path)."""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")


def load_json(path: str) -> pd.DataFrame:
    """Load JSON (expects orient that pandas can read)."""
    return pd.read_json(path)


def load_sql(db_path: str, query: str = "SELECT * FROM sales") -> pd.DataFrame:
    """Load from sqlite database using given query."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


# Map loader keys to functions
LOADERS: dict[str, Callable[..., pd.DataFrame]] = {
    "csv": load_csv,
    "json": load_json,
    "sql": load_sql,
}


def load_data(source_type: str, source: str, query: Optional[str] = None) -> pd.DataFrame:
    """
    Dispatcher to load data.
    Returns empty DataFrame if unsupported type.
    """
    key = source_type.lower()
    loader = LOADERS.get(key)
    if loader is None:
        return pd.DataFrame()
    # SQL needs query param
    if key == "sql":
        return loader(source, query if query is not None else "SELECT * FROM sales")
    return loader(source)
