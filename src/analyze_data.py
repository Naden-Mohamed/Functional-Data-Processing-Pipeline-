

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from typing import Dict, Any, Tuple, List, Callable


def _calculate_summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pure function to calculate key summary statistics for numeric columns.
    Input: DataFrame. Output: New DataFrame (the result). No side effects.
    """
    numeric_df = df.select_dtypes(include=np.number)
    
    if numeric_df.empty:
        return pd.DataFrame()

   
    stats_functions: Dict[str, Callable] = {
        'count': pd.Series.count,
        'mean': pd.Series.mean,
        'median': pd.Series.median,
        'variance': pd.Series.var,
        'std_dev': pd.Series.std,
        'min': pd.Series.min,
        'max': pd.Series.max
    }
    
    
    results_dict = {
        stat_name: numeric_df.apply(func) 
        for stat_name, func in stats_functions.items()
    }
    
    return pd.DataFrame(results_dict)


def _calculate_correlation(df: pd.DataFrame, col1: str, col2: str) -> Dict[str, Any]:
    """
    Pure function to calculate Pearson correlation and determine trend.
    Returns a dictionary of results.
    """
    if col1 not in df.columns or col2 not in df.columns:
        return {"error": f"Columns '{col1}' or '{col2}' not found."}
        
    if not (pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2])):
        return {"error": "Correlation requires both columns to be numeric."}

   
    cleaned_data = df[[col1, col2]].dropna()
    x = cleaned_data[col1]
    y = cleaned_data[col2]
    
    if len(x) < 2:
        return {"error": "Not enough data points for correlation calculation."}

   
    r, p = pearsonr(x, y)
    
  
    interpretation = (
        "Very Strong Positive Trend." if r >= 0.9 else
        "Strong Positive Trend." if r > 0.7 else
        "Moderate Positive Trend." if r > 0.3 else
        "Weak Positive Trend." if r > 0.0 else
        "Very Strong Negative Trend." if r <= -0.9 else
        "Strong Negative Trend." if r < -0.7 else
        "Moderate Negative Trend." if r < -0.3 else
        "Weak Negative Trend." if r < 0.0 else
        "No Significant Linear Trend."
    )

    return {
        "coefficient": r,
        "p_value": p,
        "interpretation": interpretation
    }


def _calculate_outliers(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """
    Pure function to calculate IQR and identify outliers.
    Returns a dictionary of bounds and outlier data.
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return {"error": f"Column '{column}' is missing or not numeric."}

    data = df[column].dropna()
    if data.empty:
        return {"error": "Column is empty after dropping NaNs."}

   
    Q1, Q3 = data.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    
    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)
    
 
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    
    return {
        "Q1": Q1, 
        "Q3": Q3, 
        "IQR": IQR,
        "lower_bound": lower_bound, 
        "upper_bound": upper_bound,
        "outliers": outliers.to_frame(),
        "total_records": len(data)
    }



def summary_statistics(df: pd.DataFrame):
    """
    1. Statistical summaries. Calls pure function and handles printing (side effect).
    """
    print("\n## 1. Calculating Summary Statistics (Functional)...")
    
   
    stats_df = _calculate_summary_stats(df)
    unique_counts = df.apply(lambda x: len(x.unique())) 

  
    if not stats_df.empty:
        print("\n--- Summary Statistics Results (Numeric Columns) ---")
        print(stats_df.round(2).to_string())
        print("--------------------------------------------------")
    else:
        print("  [WARN] No numeric columns found for full statistical summaries.")

    print("  > Calculating Unique Value Counts for all columns...")
    print("\n--- Unique Value Counts per Column ---")
    print(unique_counts.to_string())
    print("--------------------------------------")


def correlation_analysis(df: pd.DataFrame, col1: str, col2: str):
    """
    2. Correlation analysis. Calls pure function and handles printing (side effect).
    """
    print(f"\n## 2. Running Correlation Analysis for '{col1}' and '{col2}' (Functional)...")
    
   
    results = _calculate_correlation(df, col1, col2)
    
  
    if "error" in results:
        print(f"  [ERROR] {results['error']}")
        return

    r = results['coefficient']
    
    print(f"\n--- Correlation Results ({col1} vs {col2}) ---")
    print(f"  Pearson Coefficient (r): {r:.4f}")
    print(f"  Interpretation: {results['interpretation']}")
    print("---------------------------------------------")


def dataset_overview(df: pd.DataFrame):
    """
    3. Dataset summary. Handles structural calculations and printing (side effect).
    """
    print("\n## 3. Generating Dataset Overview (Functional)...")
    
    
    num_rows, num_cols = df.shape 
    
   
    missing_report = df.isnull().sum()
    missing_report = missing_report[missing_report > 0].sort_values(ascending=False)
    
 
    print(f"  > Number of Rows (Records): {num_rows}")
    print(f"  > Number of Columns (Features): {num_cols}")
    
    print("\n--- Data Types per Column ---")
    print(df.dtypes.to_string())
    
    print("\n--- Missing Value Overview ---")
    if missing_report.empty:
        print("  No missing values detected.")
    else:
        print("\n".join([f"  - {col}: {count}" for col, count in missing_report.items()]))
    print("---------------------------------")


def detect_outliers(df: pd.DataFrame, column: str):
    """
    4. Outlier detection using the IQR method. Calls pure function and handles printing (side effect).
    """
    print(f"\n## 4. Detecting Outliers in Column '{column}' using IQR (Functional)...")
    

    results = _calculate_outliers(df, column)

  
    if "error" in results:
        print(f"  [ERROR] {results['error']}")
        return

    outliers_df = results['outliers']
    num_outliers = len(outliers_df)
    total_records = results['total_records']
    
    print("\n--- IQR Outlier Detection Results ---")
    print(f"  Q1 (25th percentile): {results['Q1']:,.2f}")
    print(f"  Q3 (75th percentile): {results['Q3']:,.2f}")
    print(f"  IQR (Q3 - Q1): {results['IQR']:,.2f}")
    print(f"  Lower Bound: {results['lower_bound']:,.2f}")
    print(f"  Upper Bound: {results['upper_bound']:,.2f}")
    print(f"  Number of Outliers Detected: **{num_outliers}** ({(num_outliers / total_records * 100):.2f}%)")
    
    if num_outliers > 0:
        print("  Sample Outliers:")
        print(outliers_df.head(5).to_string())
    
    print("-------------------------------------")



if __name__ == '__main__':
 
    print("=============================================================")
    print("       STARTING analyze_data.py (FUNCTIONAL) DEMO")
    print("=============================================================")
    
   
    data = {
        'Sales': [100.0, 150.5, 95.2, 1000.0, 120.0, 110.5, 130.0, 100.0, np.nan, 140.0],
        'Cost': [50.0, 70.0, 45.0, 450.0, 60.0, 55.0, 65.0, 50.0, 70.0, np.nan],
        'Region': ['East', 'West', 'East', 'Central', 'West', 'East', 'West', 'East', 'Central', 'West'],
        'Order_Date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', 
                                     '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08',
                                     pd.NaT, '2023-01-10'])
    }
    test_df = pd.DataFrame(data)

   
    dataset_overview(test_df)
    summary_statistics(test_df)
    correlation_analysis(test_df, 'Sales', 'Cost')
    detect_outliers(test_df, 'Sales')
    
    print("\n=============================================================")
    print("          ANALYSIS MODULE DEMONSTRATION COMPLETE")
    print("=============================================================")