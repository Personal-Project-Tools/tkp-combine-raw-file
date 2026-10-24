import os
from typing import Optional

from core.reader import load_and_combine_product_files
from core.processor import create_daily_summary
from exporters.excel_exporter import (
    export_raw_data,
    export_daily_summary_to_excel,
    get_month_suffix,
)
from ui.dialogs import select_input_folder, select_working_file


def run_pipeline(
    folder_path: Optional[str] = None,
    working_file: Optional[str] = None,
    custom_month_suffix: Optional[str] = None,
) -> None:
    """Execute the end-to-end raw files consolidation and daily summary generation pipeline."""
    # Step 1: Select folder and template file if not passed directly
    if not folder_path:
        folder_path = select_input_folder()
        if not folder_path:
            return

    if not working_file:
        working_file = select_working_file()
        if not working_file:
            return

    # Step 2: Read and combine product_list files
    print(f"\nProcessing files from: {folder_path}...")
    combined_df, file_count = load_and_combine_product_files(folder_path)

    if combined_df.empty:
        print(f"No data or `product_list` files were found in {folder_path}.")
        return

    # Determine month suffix: uses custom_month_suffix if provided, otherwise auto-detects from data
    month_suffix = custom_month_suffix or get_month_suffix(combined_df["Day"])
    output_dir = os.path.dirname(working_file)

    # Step 3: Populate raw data sheet into the working template
    print(f"\nOpening template file {os.path.basename(working_file)}...")
    output_raw_file = os.path.join(output_dir, f"raw_data_{month_suffix}.xlsx")
    try:
        print("Pasting combined data into 'raw data' sheet...")
        export_raw_data(working_file, combined_df, output_raw_file)
        print(f"[1/2] Raw data file saved successfully!")
        print(f"      -> {output_raw_file}")
    except Exception as e:
        print(f"Failed to export raw data: {e}")
        return

    # Step 4: Generate and export formatted daily summary
    print("\n[2/2] Generating daily summary (aggregating metrics by day)...")
    daily_summary, final_cols = create_daily_summary(combined_df)
    output_summary_file = os.path.join(output_dir, f"daily_summary_{month_suffix}.xlsx")

    try:
        export_daily_summary_to_excel(daily_summary, final_cols, output_summary_file)
        print(f"      Daily summary file saved successfully!")
        print(f"      -> {output_summary_file}")
    except Exception as e:
        print(f"Failed to export daily summary: {e}")
        return

    print(f"\nCompleted! Successfully processed data from {file_count} files.")


if __name__ == "__main__":
    CUSTOM_MONTH_SUFFIX = 'Aug26'

    run_pipeline(custom_month_suffix=CUSTOM_MONTH_SUFFIX)

