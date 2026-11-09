
import pandas as pd
import great_expectations as gx
from pathlib import Path

# --------------------------------
# 1. Project paths
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "output" / "processed" / "online_retail_prepared.csv"
REPORT_DIR = BASE_DIR / "output" / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------
# 2. Load prepared dataset
# --------------------------------

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Total rows:", len(df))

# --------------------------------
# 3. Great Expectations setup
# --------------------------------

context = gx.get_context()

data_source = context.data_sources.add_pandas(
    name="icestream_pandas_source"
)

data_asset = data_source.add_dataframe_asset(
    name="retail_data"
)

batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "retail_batch"
)

batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

# --------------------------------
# 4. Great Expectations rules
# --------------------------------

expectations = [
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="invoice"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="stockcode"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="quantity"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="price"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="invoice_date"
    )
]

results = []

for expectation in expectations:

    result = batch.validate(expectation)

    metrics = result.result or {}

    total = metrics.get("element_count", len(df))
    unsuccessful = metrics.get("unexpected_count", 0)
    successful = total - unsuccessful

    results.append({
        "check": expectation.column + " not null",
        "total_records": total,
        "successful_records": successful,
        "unsuccessful_records": unsuccessful,
        "status": "PASS" if result.success else "FAIL"
    })

# --------------------------------
# 5. Additional data quality checks
# --------------------------------

additional_checks = [
    {
        "check": "Duplicate rows",
        "count": int(
    df[
        [
            "invoice",
            "stockcode",
            "description",
            "quantity",
            "invoice_date",
            "price",
            "customer_id",
            "country"
        ]
    ].duplicated().sum()
),
        "status": "REVIEW"
    },
    {
        "check": "Non-positive quantities",
        "count": int((df["quantity"] <= 0).sum()),
        "status": "REVIEW"
    },
    {
        "check": "Non-positive prices",
        "count": int((df["price"] <= 0).sum()),
        "status": "REVIEW"
    },
    {
        "check": "Missing customer IDs",
        "count": int(df["customer_id"].isna().sum()),
        "status": "REVIEW"
    },
    {
        "check": "Cancelled invoice rows",
        "count": int(df["is_cancelled"].sum()),
        "status": "INFO"
    }
]

for item in additional_checks:

    results.append({
        "check": item["check"],
        "total_records": len(df),
        "successful_records": len(df) - item["count"],
        "unsuccessful_records": item["count"],
        "status": item["status"]
    })

# --------------------------------
# 6. Save validation report
# --------------------------------

report = pd.DataFrame(results)

report_file = REPORT_DIR / "data_quality_report.csv"

report.to_csv(report_file, index=False)

# --------------------------------
# 7. Display results
# --------------------------------

print("\nDATA QUALITY VALIDATION REPORT")
print(report.to_string(index=False))

print("\nGreat Expectations checks passed:",
      (report["status"] == "PASS").sum())

print("Great Expectations checks failed:",
      (report["status"] == "FAIL").sum())

print("\nReport saved at:", report_file)
print("\nData quality validation completed!")
