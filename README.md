# Python Data Analyzer

A Python-based sales analytics application that transforms CSV sales data into meaningful business insights through data validation, accurate financial calculations, automated testing, and an interactive Streamlit dashboard.

## Overview

**Python Data Analyzer** is a data analysis project built with Python, Pandas, and Streamlit. It processes sales records, calculates revenue metrics, identifies product performance, and presents results through interactive charts and downloadable JSON reports.

The project combines a reusable Python analysis module with a web-based dashboard, making it easy to analyze sample data or upload a custom sales CSV file.

## Features

- **CSV data processing:** Load and validate sales records from CSV files.
- **Financial analysis:** Calculate sales revenue and summary metrics using Python's `Decimal` for accurate monetary arithmetic.
- **Business insights:** Analyze total revenue, units sold, transaction count, average record value, and product performance.
- **Interactive dashboard:** Explore sales metrics and visualizations with Streamlit.
- **Daily revenue trend:** Track revenue changes over time with a line chart.
- **Category analysis:** Compare revenue across product categories.
- **Product performance:** Identify top-performing products by revenue.
- **Interactive filters:** Filter sales by date range and product category.
- **CSV upload:** Analyze custom datasets through the dashboard.
- **JSON export:** Download an analysis report for the currently selected data.
- **Automated testing:** Verify core analysis functionality using pytest.
- **Command-line interface:** Run the analyzer directly from the terminal.

## Tech Stack

- Python
- Pandas
- Streamlit
- Decimal
- CSV and JSON


## Project Structure

```text
python-data-analyzer/
├── .streamlit/
│   └── config.toml
├── data/
│   └── sales.csv
├── tests/
│   └── test_analyzer.py
├── .gitignore
├── analyzer.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible newer version
- pip
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/ElenaHeydari/python-data-analyzer.git
cd python-data-analyzer
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If your virtual environment already exists, activate it instead of creating it again.

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Interactive Dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

The dashboard loads `data/sales.csv` by default. You can also upload your own CSV file using the sidebar.

## Command-Line Usage

Run the analyzer with the default dataset:

```bash
python analyzer.py
```

Specify an input CSV file and an output report path:

```bash
python analyzer.py --input data/sales.csv --output reports/sales_report.json
```

The output path can be changed to save the generated JSON report elsewhere.

## Input Data Format

The CSV file must contain the following columns:

| Column | Description |
|---|---|
| `date` | Sales date in `YYYY-MM-DD` format |
| `product` | Product name |
| `category` | Product category |
| `quantity` | Number of units sold |
| `unit_price` | Price per unit |

Example:

```csv
date,product,category,quantity,unit_price
2026-10-01,Laptop,Electronics,2,850.00
2026-10-01,Mouse,Accessories,5,18.50
2026-10-02,Keyboard,Accessories,3,45.00
```

The input data should contain valid values for the required fields. The analyzer validates the data before calculating metrics.

## Sample Results

Using the included sample dataset, the expected overall metrics are:

| Metric | Value |
|---|---:|
| Sales records | 12 |
| Units sold | 47 |
| Total revenue | $5,615.40 |
| Average record value | $467.95 |
| Top product by revenue | Laptop |

The figures above describe the included sample dataset before applying dashboard filters.

## Dashboard

The interactive dashboard provides:

- Revenue, units sold, record count, and average record value.
- Revenue by category.
- Top products ranked by revenue.
- Daily revenue trend visualization.
- Date and category filters.
- A sales records table.
- CSV file upload and JSON report download.


## Financial Accuracy

The analyzer uses Python's `Decimal` type for monetary calculations to reduce floating-point rounding errors.

Financial values are represented with two decimal places where appropriate. Monetary values in JSON reports are serialized as strings to preserve decimal precision.

## Future Improvements

Potential extensions include:

- Additional data quality checks and clearer validation messages.
- More advanced sales and customer analytics.
- Exporting reports to CSV and Excel.
- Improved dashboard visualizations.
- Continuous integration with automated tests.
- Online deployment for public access.

## Author

**Elena Heydari**

GitHub: [@ElenaHeydari](https://github.com/ElenaHeydari)

---
