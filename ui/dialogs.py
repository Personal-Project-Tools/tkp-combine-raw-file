import tkinter as tk
from tkinter import filedialog
from typing import Optional


def select_input_folder() -> Optional[str]:
    """Display folder picker dialog to select directory containing product_list files."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("Please select the folder containing the product_list... files")
    folder_path = filedialog.askdirectory(title="Select the folder containing the product_list files")
    root.destroy()

    if not folder_path:
        print("No folder selected. The operation has been canceled.")
        return None
    return folder_path


def select_working_file() -> Optional[str]:
    """Display file picker dialog to select working template Excel file."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    print("Please select working file (raw_file_samples.xlsx)")
    working_file = filedialog.askopenfilename(
        title="Select working file",
        filetypes=[("Excel files", "*.xlsx *.xls")],
    )
    root.destroy()

    if not working_file:
        print("No working files selected. The operation has been canceled.")
        return None
    return working_file
