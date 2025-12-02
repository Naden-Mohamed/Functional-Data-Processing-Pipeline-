# src/output.py
from typing import Any
import pandas as pd

# -------------------------
# Pure functions (build strings)
# -------------------------

def build_text_block(title: str, content: str) -> str:
    """Pure: build a formatted string block."""
    return f"\n===== {title} =====\n{content}\n====================\n"


def build_dataframe_block(df: pd.DataFrame, title: str) -> str:
    """Pure: convert DataFrame to a printable text block."""
    return build_text_block(title, df.to_string())


def build_dict_block(d: dict, title: str) -> str:
    """Pure: build display text from dictionary."""
    import json
    pretty = json.dumps(d, indent=2, default=str)
    return build_text_block(title, pretty)


# -------------------------
# Side-effect functions (print & save)
# -------------------------

def print_block(text: str) -> None:
    """Print to console (side effect)."""
    print(text)


def save_block(text: str, filename: str = "output_report.txt") -> None:
    """Append text to a file (side effect)."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")
