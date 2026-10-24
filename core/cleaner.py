import re
from typing import Any
import pandas as pd


def clean_numeric(val: Any) -> float:
    """Clean string values with currency (Rp), percentage (%), hyphens (-), and separators to float."""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)

    s = str(val).strip()
    if s in ("-", "", "nan") or s.lower() == "nan":
        return 0.0

    if "Rp" in s:
        s = s.replace("Rp", "").replace(".", "").replace(",", ".").strip()
    elif "%" in s:
        s = s.replace("%", "").strip()
    else:
        s = s.replace(",", "")

    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def extract_date_from_excel(file_path: str) -> str:
    """Extract date string (YYYY-MM-DD) from the first cell (A1) of an Excel file."""
    df_raw = pd.read_excel(file_path, header=None, nrows=1)
    date_raw_string = str(df_raw.iloc[0, 0])

    match = re.search(r"(\d{4}-\d{2}-\d{2})", date_raw_string)
    return match.group(1) if match else date_raw_string
