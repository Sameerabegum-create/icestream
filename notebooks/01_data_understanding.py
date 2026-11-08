
import pandas as pd
from pathlib import Path

# ==========================================
# ICESTREAM - DATASET UNDERSTANDING
# ==========================================

print("=" * 60)
print("       ICESTREAM - DATASET ANALYSIS")
print("=" * 60)

# 1. Locate the project and dataset
BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "dataset" / "online_retail_II.xlsx"

# 2. Check dataset availability
if not FILE_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {FILE_PATH}"
    )

print("\nDataset found successfully!")

# 3. Identify Excel sheets
excel = pd.ExcelFile(FILE_PATH)

print("\nAvailable Excel Sheets:")
print(excel.sheet_names)

# 4. Analyze each sheet
for sheet in excel.sheet_names:

    print("\n" + "=" * 60)
    print(f"ANALYSIS OF SHEET: {sheet}")
    print("=" * 60)

    # Load sheet
    df = pd.read_excel(FILE_PATH, sheet_name=sheet)

    # 5. Dataset information
    print("\n1. First 5 Records:")
    print(df.head())

    print("\n2. Last 5 Records:")
    print(df.tail())

    print("\n3. Dataset Shape:")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\n4. Column Names:")
    print(df.columns.tolist())

    print("\n5. Data Types:")
    print(df.dtypes)

    # 6. Missing value analysis
    print("\n6. Missing Values:")
    print(df.isnull().sum())

    print("\nMissing Value Percentage:")
    print((df.isnull().mean() * 100).round(2))

    # 7. Duplicate analysis
    print("\n7. Duplicate Records:")
    print(df.duplicated().sum())

    # 8. Quantity analysis
    print("\n8. Negative Quantity Records:")
    print((df["Quantity"] < 0).sum())

    print("\nZero Quantity Records:")
    print((df["Quantity"] == 0).sum())

    # 9. Price analysis
    print("\n9. Zero or Negative Prices:")
    print((df["Price"] <= 0).sum())

    # 10. Customer analysis
    print("\n10. Missing Customer IDs:")
    print(df["Customer ID"].isnull().sum())

    print("\nUnique Customers:")
    print(df["Customer ID"].nunique())

    # 11. Invoice analysis
    cancelled = df["Invoice"].astype(str).str.startswith("C")

    print("\n11. Cancelled Invoice Records:")
    print(cancelled.sum())

    print("\nUnique Products:")
    print(df["StockCode"].nunique())

    print("\nUnique Invoices:")
    print(df["Invoice"].nunique())

    # 12. Date analysis
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    print("\n12. Date Range:")
    print("Start Date:", df["InvoiceDate"].min())
    print("End Date:", df["InvoiceDate"].max())

    # 13. Sales analysis
    df["Sales"] = df["Quantity"] * df["Price"]

    print("\n13. Total Sales Value:")
    print(round(df["Sales"].sum(), 2))

    # 14. Statistical summary
    print("\n14. Statistical Summary:")
    print(df.describe())

print("\n" + "=" * 60)
print("       DATASET ANALYSIS COMPLETED")
print("=" * 60)
