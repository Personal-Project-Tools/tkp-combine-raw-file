import glob
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional


def detect_working_file(search_dir: Optional[str] = None) -> Optional[str]:
    """
    Auto-detect raw working template file in the specified directory (or project root).
    Searches for files like raw_file_sample.xlsx, raw_file*.xlsx, etc.
    Returns the absolute path if found, otherwise None.
    """
    if not search_dir:
        # Default to project root (parent directory of ui/)
        search_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Priority 1: Check exact well-known template names
    priority_names = [
        "raw_file_sample.xlsx",
        "raw_file_samples.xlsx",
        "raw_file.xlsx",
        "raw_sample.xlsx",
    ]
    for name in priority_names:
        candidate = os.path.join(search_dir, name)
        if os.path.isfile(candidate):
            return candidate

    # Priority 2: Pattern match raw_file*.xlsx or raw*.xlsx
    patterns = ["raw_file*.xlsx", "raw_file*.xls", "raw*.xlsx", "raw*.xls"]
    for pattern in patterns:
        for match in glob.glob(os.path.join(search_dir, pattern)):
            filename = os.path.basename(match)
            # Exclude temp files and output files
            if filename.startswith("~$") or filename.startswith("raw_data_") or filename.startswith("daily_summary_"):
                continue
            if os.path.isfile(match):
                return match

    # Also check current working directory if different from project root
    cwd = os.getcwd()
    if os.path.abspath(cwd) != os.path.abspath(search_dir):
        for name in priority_names:
            candidate = os.path.join(cwd, name)
            if os.path.isfile(candidate):
                return candidate
        for pattern in patterns:
            for match in glob.glob(os.path.join(cwd, pattern)):
                filename = os.path.basename(match)
                if filename.startswith("~$") or filename.startswith("raw_data_") or filename.startswith("daily_summary_"):
                    continue
                if os.path.isfile(match):
                    return match

    return None


def select_input_folder(initialdir: Optional[str] = None) -> Optional[str]:
    """Display folder picker dialog to select directory containing product_list files."""
    if not initialdir:
        initialdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("Please select the folder containing the product_list... files")
    folder_path = filedialog.askdirectory(
        title="Select the folder containing the product_list files",
        initialdir=initialdir,
    )
    root.destroy()

    if not folder_path:
        print("No folder selected. The operation has been canceled.")
        return None
    return folder_path


def select_working_file(initialdir: Optional[str] = None) -> Optional[str]:
    """Display file picker dialog to select working template Excel file."""
    if not initialdir:
        initialdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("Please select working file (raw_file_samples.xlsx)")
    working_file = filedialog.askopenfilename(
        title="Select working file",
        initialdir=initialdir,
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    root.destroy()

    if not working_file:
        print("No working files selected. The operation has been canceled.")
        return None
    return working_file

