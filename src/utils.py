# src/utils.py
from typing import Dict, Any
import pandas as pd

def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a small info dict about the DataFrame (pure)."""
    return {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
        "missing_values": {k: int(v) for k, v in df.isna().sum().to_dict().items()},
        "head": df.head().to_dict(orient="records")
    }
