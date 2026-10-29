
import csv
import json
import tempfile
import unittest
from pathlib import Path

from analyzer import analyze_sales, load_sales, save_report
from decimal import Decimal

class TestSalesAnalyzer(unittest.TestCase):

    def setUp(self):
        self.sales = [
            {
                "date": "2026-10-01",
                "product": "Laptop",
                "category": "Electronics",
                "quantity": 2,
                "unit_price": Decimal(850.00),
                "revenue": Decimal(1700.00),
            },
            {
                "date": "2026-10-01",
                "product": "Mouse",
                "category": "Accessories",
                "quantity": 5,
                "unit_price": Decimal(18.50),
                "revenue": Decimal(92.50),
            },
            {
                "date": "2026-10-02",
                "product": "Laptop",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": Decimal(850.00),
                "revenue": Decimal(850.00),
            },
        ]

        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def test_total_revenue(self):
        report = analyze_sales(self.sales)
        self.assertEqual(report["total_revenue"], "2642.50")

    def test_total_units_sold(self):
        report = analyze_sales(self.sales)
        self.assertEqual(report["total_units_sold"], 8)

    def test_transaction_count(self):
        report = analyze_sales(self.sales)
        self.assertEqual(report["transaction_count"], 3)

    def test_top_product_by_revenue(self):
        report = analyze_sales(self.sales)
        self.assertEqual(
            report["top_product_by_revenue"]["name"],
            "Laptop",
        )
        self.assertEqual(
            report["top_product_by_revenue"]["revenue"],
            "2550.00",
        )

    def test_revenue_by_category(self):
        report = analyze_sales(self.sales)
        self.assertEqual(
            report["revenue_by_category"]["Electronics"],
            "2550.00",
        )
        self.assertEqual(
            report["revenue_by_category"]["Accessories"],
            "92.50",
        )

    def test_empty_sales_list_raises_error(self):
        with self.assertRaises(ValueError):
            analyze_sales([])

    def test_missing_csv_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            load_sales(self.temp_path / "missing.csv")

    def test_invalid_quantity_is_rejected(self):
        csv_path = self.temp_path / "invalid.csv"

        with csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["date", "product", "category", "quantity", "unit_price"]
            )
            writer.writerow(
                ["2026-10-01", "Laptop", "Electronics", "-2", "850.00"]
            )

        with self.assertRaisesRegex(ValueError, "row 2"):
            load_sales(csv_path)

    def test_report_is_saved_as_json(self):
        report = analyze_sales(self.sales)
        output_path = self.temp_path / "reports" / "report.json"

        saved_path = save_report(report, output_path)

        self.assertTrue(saved_path.is_file())

        with saved_path.open(encoding="utf-8") as file:
            saved_report = json.load(file)

        self.assertEqual(saved_report["total_revenue"], "2642.50")
        
    def test_decimal_money_is_accurate(self):
        sales = [
            {
                "date": "2026-10-01",
                "product": "Cable",
                "category": "Accessories",
                "quantity": 3,
                "unit_price": Decimal("0.10"),
                "revenue": Decimal("0.30"),
            }
        ]

        report = analyze_sales(sales)

        self.assertEqual(report["total_revenue"], "0.30")


if __name__ == "__main__":
    unittest.main()
