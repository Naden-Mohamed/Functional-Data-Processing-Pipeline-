# main.py
from src.load_data import load_data
from src.clean_data import auto_handle_missing
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

def run_pipeline(
    source_type: str,
    source: str,
    correlation_cols: tuple[str, str] | None = ("Sales", "Profit"),
    outlier_column: str | None = "Sales"
) -> dict:
    """
    Pure-ish orchestrator returning a dict of results.
    Side effects only done outside this function.
    """
    # 1. Load
    df = load_data(source_type, source)

    # 2. Clean
    cleaned_df = auto_handle_missing(df)

    # 3. Analyses (pure functions)
    info = get_data_info(cleaned_df)
    overview = dataset_overview(cleaned_df)
    summary_stats = calculate_summary_stats(cleaned_df)
    unique_counts = calculate_unique_counts(cleaned_df)

    correlation_result = None
    if correlation_cols:
        correlation_result = calculate_correlation(cleaned_df, correlation_cols[0], correlation_cols[1])

    outliers_result = None
    if outlier_column:
        outliers_result = calculate_outliers_iqr(cleaned_df, outlier_column)

    # 4. Return everything (no printing or file writes here)
    return {
        "cleaned_df": cleaned_df,
        "info": info,
        "overview": overview,
        "summary_stats": summary_stats,
        "unique_counts": unique_counts,
        "correlation": correlation_result,
        "outliers": outliers_result
    }


def main():
    # configure paths
    source_type = "csv"
    source = "Data/Row/Sample - Superstore.csv"  # update to your path

    results = run_pipeline(source_type, source, correlation_cols=("Sales", "Profit"), outlier_column="Sales")

    # Save cleaned CSV (side effect)
    results["cleaned_df"].to_csv("clean_data.csv", index=False)

    # Build output text (pure builders)
    info_text = build_dict_block(results["info"], "DATA INFO")
    overview_text = build_dict_block(results["overview"], "DATASET OVERVIEW")
    summary_text = build_dataframe_block(results["summary_stats"], "SUMMARY STATISTICS")
    unique_text = build_text_block("UNIQUE COUNTS", results["unique_counts"].to_string())
    corr_text = build_text_block("CORRELATION", str(results["correlation"]))
    outlier_text = build_text_block("OUTLIERS", str(results["outliers"]))

    # Print & Save (side effects)
    for block in (info_text, overview_text, summary_text, unique_text, corr_text, outlier_text):
        print_block(block)
        save_block(block, filename="clean_output.txt")

    print_block(build_text_block("FILE_SAVED", "clean_data.csv saved successfully"))
    save_block("clean_data.csv saved successfully", filename="clean_output.txt")


if __name__ == "__main__":
    main()
