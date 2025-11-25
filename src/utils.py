import pandas as pd
from typing import Dict, Any

def get_data_info(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "shape": {"rows": df.shape[0], "columns": df.shape[1]},
        "dtypes": df.dtypes.to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "head": df.head().to_dict(orient="records")
    }