from typing import Dict, Any
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# ================================
# Analysis Functions (Pure)
# ================================

def calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return DataFrame with common stats for numeric columns."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        return pd.DataFrame()
    stats = pd.DataFrame({
        "count": numeric_df.count(),
        "mean": numeric_df.mean(),
        "median": numeric_df.median(),
        "variance": numeric_df.var(ddof=1),
        "std_dev": numeric_df.std(ddof=1),
        "min": numeric_df.min(),
        "max": numeric_df.max()
    })
    return stats.T  # rows = stats, columns = numeric columns

def calculate_unique_counts(df: pd.DataFrame) -> pd.Series:
    """Return Series of unique value counts per column."""
    return df.apply(lambda s: s.nunique())

def calculate_correlation(df: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
    """Calculate Pearson correlation coefficient and p-value."""
    if col1 not in df.columns or col2 not in df.columns:
        return {"error": f"Columns '{col1}' or '{col2}' not found."}
    if not (pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2])):
        return {"error": "Correlation requires numeric columns."}
    cleaned = df[[col1, col2]].dropna()
    if len(cleaned) < 2:
        return {"error": "Not enough data points."}
    r, p = pearsonr(cleaned[col1], cleaned[col2])
    abs_r = abs(r)
    strength = "Very Strong" if abs_r >= 0.9 else "Strong" if abs_r >= 0.7 else "Moderate" if abs_r >= 0.3 else "Weak" if abs_r > 0 else "No"
    direction = "Positive" if r > 0 else "Negative" if r < 0 else "None"
    interpretation = f"{strength} {direction} Trend." if strength != "No" else "No Significant Linear Trend."
    return {"coefficient": float(r), "p_value": float(p), "interpretation": interpretation}

def calculate_outliers_iqr(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Detect outliers using IQR method."""
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return {"error": f"Column '{column}' is missing or not numeric."}
    data = df[column].dropna()
    if data.empty:
        return {"error": "Column empty."}
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = data[(data < lower) | (data > upper)]
    return {
        "Q1": float(Q1),
        "Q3": float(Q3),
        "IQR": float(IQR),
        "lower_bound": float(lower),
        "upper_bound": float(upper),
        "outliers": outliers.to_dict(),
        "total_records": int(len(data))
    }

def dataset_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """Return overview dictionary with rows, columns, dtypes, missing."""
    num_rows, num_cols = df.shape
    missing_report = df.isnull().sum()
    missing_report = missing_report[missing_report > 0].sort_values(ascending=False).to_dict()
    return {
        "rows": int(num_rows),
        "columns": int(num_cols),
        "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
        "missing": {k: int(v) for k, v in missing_report.items()}
    }
