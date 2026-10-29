
import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

REQUIRED_COLUMNS = {
    "date",
    "product",
    "category",
    "quantity",
    "unit_price",
}

def parse_money(value):
    """Parse a monetary value accurately to two decimal places."""
    try:
        amount = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(f"Invalid monetary value: {value!r}")

    if not amount.is_finite() or amount < 0:
        raise ValueError("Unit price must be a finite, non-negative number.")

    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def load_sales(csv_path):
    """Load sales records from a CSV file and validate the data."""
    csv_path = Path(csv_path)

    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no header.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns: {missing}")

        sales = []

        for row_number, row in enumerate(reader, start=2):
            try:
                sale_date = date.fromisoformat(row["date"].strip())
                product = row["product"].strip()
                category = row["category"].strip()
                quantity = int(row["quantity"])
                unit_price = parse_money(row["unit_price"])

                if not product:
                    raise ValueError("Product name cannot be empty.")

                if not category:
                    raise ValueError("Category cannot be empty.")

                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")

                if not unit_price >= 0 or unit_price == float("inf"):
                    raise ValueError("Unit price must be non-negative.")

                if unit_price != unit_price:
                    raise ValueError("Unit price must be a valid number.")

            except (ValueError, AttributeError, TypeError) as error:
                raise ValueError(
                    f"Invalid data on CSV row {row_number}: {error}"
                ) from error

            sales.append(
                {
                    "date": sale_date.isoformat(),
                    "product": product,
                    "category": category,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "revenue": (unit_price * quantity).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    ),
                }
            )

    if not sales:
        raise ValueError("CSV file contains no sales records.")

    return sales



def analyze_sales(sales):
    """Calculate accurate sales statistics from validated records."""
    if not sales:
        raise ValueError("Cannot analyze an empty sales list.")

    total_revenue = sum(
        (sale["revenue"] for sale in sales),
        Decimal("0.00"),
    )
    total_units = sum(sale["quantity"] for sale in sales)

    product_stats = defaultdict(
        lambda: {"quantity": 0, "revenue": Decimal("0.00")}
    )
    category_revenue = defaultdict(lambda: Decimal("0.00"))

    for sale in sales:
        product = sale["product"]
        category = sale["category"]

        product_stats[product]["quantity"] += sale["quantity"]
        product_stats[product]["revenue"] += sale["revenue"]
        category_revenue[category] += sale["revenue"]

    top_product_by_revenue = max(
        product_stats,
        key=lambda name: product_stats[name]["revenue"],
    )
    top_product_by_quantity = max(
        product_stats,
        key=lambda name: product_stats[name]["quantity"],
    )

    average_transaction_value = (
        total_revenue / Decimal(len(sales))
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "transaction_count": len(sales),
        "total_units_sold": total_units,
        "total_revenue": format(total_revenue, ".2f"),
        "average_transaction_value": format(
            average_transaction_value, ".2f"
        ),
        "top_product_by_revenue": {
            "name": top_product_by_revenue,
            "revenue": format(
                product_stats[top_product_by_revenue]["revenue"], ".2f"
            ),
        },
        "top_product_by_quantity": {
            "name": top_product_by_quantity,
            "quantity": product_stats[top_product_by_quantity]["quantity"],
        },
        "revenue_by_category": {
            category: format(revenue, ".2f")
            for category, revenue in sorted(category_revenue.items())
        },
    }



def save_report(report, output_path):
    """Save an analysis report as formatted JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Analyze sales data from a CSV file."
    )
    parser.add_argument(
        "--input",
        default="data/sales.csv",
        help="Path to the input CSV file.",
    )
    parser.add_argument(
        "--output",
        default="reports/sales_report.json",
        help="Path to the output JSON report.",
    )
    args = parser.parse_args()

    try:
        sales = load_sales(args.input)
        report = analyze_sales(sales)
        output_path = save_report(report, args.output)
    except (FileNotFoundError, ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")

    print("Sales analysis completed successfully!")
    print(f"Transactions: {report['transaction_count']}")
    print(f"Units sold: {report['total_units_sold']}")
    print(
        f"Total revenue: "
        f"${Decimal(report['total_revenue']):,.2f}"
    )
    print(
        "Top product by revenue: "
        f"{report['top_product_by_revenue']['name']}"
    )
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
