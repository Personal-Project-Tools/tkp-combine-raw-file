# TKP Combine Raw File

Automated data pipeline for consolidating daily e-commerce product performance reports (`product_list*.xlsx`), populating working Excel templates, and generating styled executive daily summaries.

---

## 📌 Features

- **Batch Ingestion**: Automatically scans, reads, and consolidates multiple daily `product_list*.xlsx` files.
- **Accurate ID Handling**: Preserves product IDs as text to prevent scientific notation or truncation.
- **Data Cleaning**: Strips currency prefixes (`Rp`), percentages (`%`), hyphens (`-`), and thousands separators into clean floating-point numbers.
- **Rate Recalculation**: Accurately recalculates Click-Through Rates (CTR) and Conversion Rates (CR) across daily summaries and totals rather than averaging percentages:
  - Video Click-Through Rate & Conversion Rate
  - Product Card Click-Through Rate & Conversion Rate
- **Executive-Grade Excel Styling**:
  - Distinct headers with custom fill (`#1F4E79`) and white bold text.
  - Formatted numbers (`0.00%` for rates, `#,##0` for counts and GMV).
  - Summary total row with double-line accounting border (`#595959`) and highlight fill (`#D9E1F2`).
  - Auto-adjusted column widths and frozen panes (`B2`).
- **Flexible Execution**: Run interactively via Tkinter dialogs or headless in scripts/pipelines.

---

## 📁 Project Structure

```text
tkp-combine-raw-file/
│
├── main.py                     # Primary pipeline entry point
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
│
├── core/                       # Core data processing logic
│   ├── cleaner.py              # Value parsing, regex dates, numeric cleaning
│   ├── reader.py               # Batch file scanner and DataFrame consolidator
│   └── processor.py            # Daily summary aggregation and rate recalculations
│
├── exporters/                  # Excel formatting and export handlers
│   ├── styles.py               # OpenPyXL design system (fonts, fills, borders, formats)
│   └── excel_exporter.py       # Raw data sheet writer and styled summary exporter
│
└── ui/                         # User interface components
    └── dialogs.py              # Tkinter folder and file selection dialogs
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8 or higher
- Required packages: `pandas`, `openpyxl`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Usage

#### Interactive Mode (GUI)
Run `main.py` directly:
1. Select the folder containing your daily `product_list*.xlsx` files via the dialog.
2. The working template file (`raw_file_sample.xlsx`) located in the root directory is **automatically detected**. If not found, a file picker will prompt you to select one.

```bash
python main.py
```

#### Programmatic / Script Mode
Import `run_pipeline` in your custom script to run headlessly without popups:

```python
from main import run_pipeline

run_pipeline(
    folder_path="path/to/product_list_folder",
    working_file="path/to/raw_file_sample.xlsx",  # Optional: auto-detects if None
    output_dir="output"                          # Optional: defaults to 'output/' folder
)
```

---

## 📊 Output Files

Outputs are saved automatically in the `output/` directory:

1. **`raw_data_<MonthYear>.xlsx`**: Template workbook with all raw consolidated records written to the `raw data` sheet.
2. **`daily_summary_<MonthYear>.xlsx`**: Styled daily performance metrics with auto-fitted column widths, frozen headers, and calculated totals.


---

## 🛠️ Modules Reference

| Module | Responsibility | Key Functions |
| :--- | :--- | :--- |
| [`core.cleaner`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/core/cleaner.py) | Data normalization | `clean_numeric`, `extract_date_from_excel` |
| [`core.reader`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/core/reader.py) | File discovery & loading | `load_and_combine_product_files` |
| [`core.processor`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/core/processor.py) | Aggregation & rate calculation | `create_daily_summary`, `calculate_total_summary` |
| [`exporters.styles`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/exporters/styles.py) | Design tokens for Excel | Fonts, Fills, Borders, Dimensions |
| [`exporters.excel_exporter`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/exporters/excel_exporter.py) | OpenPyXL workbook generation | `export_raw_data`, `export_daily_summary_to_excel` |
| [`ui.dialogs`](file:///e:/ada_tools/TKP/tkp-combine-raw-file/ui/dialogs.py) | User selection dialogs | `select_input_folder`, `select_working_file` |
