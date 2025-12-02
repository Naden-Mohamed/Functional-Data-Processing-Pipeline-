def build_text_block(title: str, content: str) -> str:
    """Build formatted text block."""
    return f"\n=== {title} ===\n{content}\n"

def build_dataframe_block(df, title: str) -> str:
    """Build text block for DataFrame."""
    return f"\n=== {title} ===\n{df.to_string()}\n"

def build_dict_block(d: dict, title: str) -> str:
    """Build text block for dictionary."""
    lines = [f"{k}: {v}" for k, v in d.items()]
    return f"\n=== {title} ===\n" + "\n".join(lines) + "\n"

def print_block(block: str):
    """Side effect: print block."""
    print(block)

def save_block(block: str, filename: str):
    """Side effect: save block to file."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(block + "\n")
