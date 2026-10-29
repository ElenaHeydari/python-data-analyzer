# Python Data Analyzer

A lightweight Python application for analyzing sales data from CSV files and generating structured JSON reports.

## Features

- Load sales records from CSV files.
- Validate required columns, dates, quantities, and prices.
- Calculate total revenue and units sold.
- Identify the top products by revenue and quantity.
- Summarize revenue by product category.
- Calculate average revenue per CSV transaction row.
- Use Python's `Decimal` for accurate monetary calculations.
- Export analysis results to JSON.
- Run automated tests with `unittest`.

## Project Structure

```text
python-data-analyzer/
├── data/
│   └── sales.csv
├── reports/
├── tests/
│   └── test_analyzer.py
├── analyzer.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or later
- No third-party packages are required for the core application.

## Getting Started

### 1. Clone the repository

```bash
cd python-data-analyzer
```

### 2. Run the analyzer

```bash
python analyzer.py
```

By default, the application reads `data/sales.csv` and writes its report to `reports/sales_report.json`.

### 3. Use custom file paths

```bash
python analyzer.py --input data/sales.csv --output reports/custom_report.json
```

### 4. Run the tests

```bash
python -m unittest discover -s tests -v
```

## Sample Output

```text
Sales analysis completed successfully!
Transactions: 12
Units sold: 47
Total revenue: $5,615.40
Top product by revenue: Laptop
Report saved to: reports/sales_report.json
```

## Example Report

```json
{
    "transaction_count": 12,
    "total_units_sold": 47,
    "total_revenue": "5615.40",
    "average_transaction_value": "467.95",
    "top_product_by_revenue": {
        "name": "Laptop",
        "revenue": "3400.00"
    }
}
```

The report contains additional fields, including the top product by quantity and revenue grouped by category.

## Data Format

The CSV input must include these columns:

| Column | Description |
|---|---|
| `date` | Sale date in `YYYY-MM-DD` format |
| `product` | Product name |
| `category` | Product category |
| `quantity` | Positive integer quantity sold |
| `unit_price` | Non-negative unit price |

Sample data is provided in `data/sales.csv`.

## Technical Highlights

- Modular Python functions
- CSV and JSON file processing
- Input validation and error handling
- Accurate decimal arithmetic for money
- Automated unit testing
- Command-line arguments with `argparse`


## Interactive Dashboard

The project includes a Streamlit dashboard for exploring sales data.

### Run the dashboard

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py
```

Open the local URL shown in your terminal.

### Dashboard Features

- Revenue and sales summary metrics
- Revenue by category and product charts
- Date and category filters
- CSV file upload
- Downloadable JSON analysis reports


## Future Improvements

- Exportable CSV summaries
- Additional reporting metrics

## License

This project is available for portfolio and educational purposes.
