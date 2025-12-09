from src.load_data import load_data
from src.clean_data import auto_handle_missing
from src.visualize_data import build_visuals, show_and_save_plots

from src.analyze_data import (
    dataset_overview,
    calculate_summary_stats,
    calculate_unique_counts,
    calculate_correlation,
    calculate_outliers_iqr
)
from src.output_data import (
    build_text_block,
    build_dataframe_block,
    build_dict_block,
    print_block,
    save_block
)
from src.utils import get_data_info

# ================================
# Pipeline orchestration (Pure-ish)
# ================================
def run_pipeline(source_type, source, correlation_cols=("Sales","Profit"), outlier_column="Sales"):
    df = load_data(source_type, source)
    cleaned_df = auto_handle_missing(df)
    return {
        "cleaned_df": cleaned_df,
        "info": get_data_info(cleaned_df),
        "overview": dataset_overview(cleaned_df),
        "summary_stats": calculate_summary_stats(cleaned_df),
        "unique_counts": calculate_unique_counts(cleaned_df),
        "correlation": calculate_correlation(cleaned_df, correlation_cols[0], correlation_cols[1]) if correlation_cols else None,
        "outliers": calculate_outliers_iqr(cleaned_df, outlier_column) if outlier_column else None
    }

def main():
    results = run_pipeline("csv", "Data/Row/Sample - Superstore.csv")

    # Save cleaned CSV
    results["cleaned_df"].to_csv("clean_data.csv", index=False)

    # Build output blocks
    blocks = [
        build_dict_block(results["info"], "DATA INFO"),
        build_dict_block(results["overview"], "DATASET OVERVIEW"),
        build_dataframe_block(results["summary_stats"], "SUMMARY STATISTICS"),
        build_text_block("UNIQUE COUNTS", results["unique_counts"].to_string()),
        build_text_block("CORRELATION", str(results["correlation"])),
        build_text_block("OUTLIERS", str(results["outliers"])),
        build_text_block("FILE_SAVED", "clean_data.csv saved successfully")
    ]

    # Print & save functionally using map
    list(map(lambda b: (print_block(b), save_block(b, "clean_output.csv ")), blocks))

    tasks = [
        {"type": "line", "x": "Sales", "y": "Profit"},
        {"type": "bar", "column": "Category"},
        {"type": "hist", "column": "Sales"},
        {"type": "scatter", "x": "Sales", "y": "Profit"}
    ]

    figures = build_visuals(tasks, results["cleaned_df"])

    # Save charts
    show_and_save_plots(figures)

    
if __name__ == "__main__":
    main()
