
import pandas as pd
from pathlib import Path

# Get project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
INPUT_FILE = BASE_DIR / "dataset" / "online_retail_II.xlsx"

# Output directory
OUTPUT_DIR = BASE_DIR / "output" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Read both Excel sheets
sheet_1 = pd.read_excel(INPUT_FILE, sheet_name="Year 2009-2010")
sheet_2 = pd.read_excel(INPUT_FILE, sheet_name="Year 2010-2011")

# Combine both datasets
df = pd.concat([sheet_1, sheet_2], ignore_index=True)

print("Combined dataset shape:", df.shape)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)
# Rename InvoiceDate to invoice_date
df.rename(columns={"invoicedate": "invoice_date"}, inplace=True)

# Convert data types
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce")
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

# Clean text columns
for column in ["invoice", "stockcode", "description", "country"]:
    df[column] = df[column].astype("string").str.strip()

# Create monitoring columns
df["line_value"] = df["quantity"] * df["price"]
df["is_cancelled"] = df["invoice"].str.startswith("C", na=False)
df["is_duplicate"] = df.duplicated(keep="first")

# Save prepared dataset
output_file = OUTPUT_DIR / "online_retail_prepared.csv"
df.to_csv(output_file, index=False)

print("\nData preparation completed!")
print("Total rows:", len(df))
print("Saved file:", output_file)
print("Duplicate rows:", df["is_duplicate"].sum())
print("Cancelled rows:", df["is_cancelled"].sum())
print("Missing customer IDs:", df["customer_id"].isna().sum())
print("Missing descriptions:", df["description"].isna().sum())
