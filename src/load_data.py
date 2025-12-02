import pandas as pd
import sqlite3
from typing import Callable

# ================================
# Load Data Functions (Pure)
# ================================

def load_csv(path: str) -> pd.DataFrame:
    """
    Load CSV file. Try UTF-8 first, fallback to Latin-1.
    Pure function: returns DataFrame.
    """
    try:
        return pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding='latin-1')

def load_json(path: str) -> pd.DataFrame:
    """Load JSON file as DataFrame."""
    return pd.read_json(path)

def load_sql(db_path: str, query: str = "SELECT * FROM sales") -> pd.DataFrame:
    """Load SQL query from SQLite database."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)

# Mapping source type to loader function
LOADERS = {
    'csv': load_csv,
    'json': load_json,
    'sql': load_sql,
}

def load_data(source_type: str, source: str, query: str | None = None) -> pd.DataFrame:
    """
    Pure orchestrator: pick correct loader based on type.
    """
    loader: Callable = LOADERS.get(source_type.lower(), lambda x: pd.DataFrame())
    if source_type.lower() == 'sql' and query:
        return loader(source, query)
    return loader(source)
