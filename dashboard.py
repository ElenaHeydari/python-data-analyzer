
import json
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd
import streamlit as st

from analyzer import analyze_sales, load_sales


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = BASE_DIR / "data" / "sales.csv"

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Analytics Dashboard")
st.caption("Explore sales performance, revenue, and product trends.")

# Sidebar: data source
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload a sales CSV file",
    type=["csv"],
    help="Required columns: date, product, category, quantity, unit_price",
)

# Load and validate the source data
try:
    if uploaded_file is not None:
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=".csv",
                delete=False,
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = Path(temp_file.name)

            sales = load_sales(temp_path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
    else:
        sales = load_sales(DEFAULT_CSV)

except (ValueError, OSError) as error:
    st.error(f"Could not load sales data: {error}")
    st.info("Check the CSV columns and make sure all records are valid.")
    st.stop()

if not sales:
    st.warning("No sales records are available.")
    st.stop()

# Sidebar: filters
st.sidebar.header("Filters")

available_dates = [
    date.fromisoformat(sale["date"]) for sale in sales
]
min_date = min(available_dates)
max_date = max(available_dates)

date_range = st.sidebar.date_input(
    "Sales date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

categories = sorted({sale["category"] for sale in sales})
selected_categories = st.sidebar.multiselect(
    "Categories",
    options=categories,
    default=categories,
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

filtered_sales = [
    sale
    for sale in sales
    if start_date <= date.fromisoformat(sale["date"]) <= end_date
    and sale["category"] in selected_categories
]

if not filtered_sales:
    st.warning("No records match the selected filters.")
    st.stop()

# Analyze exactly the records selected by the filters
report = analyze_sales(filtered_sales)
df = pd.DataFrame(filtered_sales)

df["date"] = pd.to_datetime(df["date"])
df["unit_price"] = df["unit_price"].map(float)
df["revenue"] = df["revenue"].map(float)

# Metrics
st.subheader("Sales Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${Decimal(report['total_revenue']):,.2f}",
)
col2.metric(
    "Units Sold",
    f"{report['total_units_sold']:,}",
)
col3.metric(
    "Sales Records",
    f"{report['transaction_count']:,}",
)
col4.metric(
    "Average Record Value",
    f"${Decimal(report['average_transaction_value']):,.2f}",
)

st.divider()

# Charts
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Revenue by Category")

    category_chart = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_chart)

with right_col:
    st.subheader("Top Products by Revenue")

    product_chart = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(product_chart)


# Daily revenue trend
st.divider()
st.subheader("Daily Revenue Trend")

daily_revenue = (
    df.groupby("date")["revenue"]
    .sum()
    .sort_index()
)

st.line_chart(
    daily_revenue,
    x_label="Date",
    y_label="Revenue ($)",
)

# Sales table
st.subheader("Sales Records")

display_df = df.sort_values("date", ascending=False).copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df["unit_price"] = display_df["unit_price"].map(
    lambda value: f"${value:,.2f}"
)
display_df["revenue"] = display_df["revenue"].map(
    lambda value: f"${value:,.2f}"
)

display_df = display_df.rename(
    columns={
        "date": "Date",
        "product": "Product",
        "category": "Category",
        "quantity": "Quantity",
        "unit_price": "Unit Price",
        "revenue": "Revenue",
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)

# Download filtered analysis
st.subheader("Export Report")

report_json = json.dumps(report, indent=4, ensure_ascii=False)

st.download_button(
    label="Download filtered report (JSON)",
    data=report_json,
    file_name="sales_report.json",
    mime="application/json",
)

st.caption(
    "Average Record Value is calculated per CSV row, "
    "not per unique customer order."
)
