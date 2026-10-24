import glob
import os
from typing import Tuple
import pandas as pd
from core.cleaner import extract_date_from_excel


def load_and_combine_product_files(folder_path: str) -> Tuple[pd.DataFrame, int]:
    """
    Search for product_list*.xlsx files in folder_path, extract date,
    read records (header at row 3, ID column as string), and combine into a single DataFrame.
    """
    search_pattern = os.path.join(folder_path, "product_list*.xlsx")
    product_files = glob.glob(search_pattern)

    all_data = []

    for file in product_files:
        try:
            date_val = extract_date_from_excel(file)

            # Read with header at row index 2 (row 3 in Excel) to preserve column names
            # Force first column (Column 0 - ID) to string to prevent truncation
            df_data = pd.read_excel(file, header=2, dtype={0: str})
            df_data.insert(0, "Day", date_val)
            all_data.append(df_data)
        except Exception as e:
            print(f"Error when reading {os.path.basename(file)}: {e}")

    if not all_data:
        return pd.DataFrame(), len(product_files)

    combined_df = pd.concat(all_data, ignore_index=True)

    # Sort descending by Day
    combined_df["Sort_Date"] = pd.to_datetime(combined_df["Day"], errors="coerce")
    combined_df = combined_df.sort_values(by="Sort_Date", ascending=False).drop(columns=["Sort_Date"])

    return combined_df, len(product_files)
