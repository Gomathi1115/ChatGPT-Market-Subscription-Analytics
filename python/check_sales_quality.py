
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
data_folder = project_path / "data" / "raw"

sales_files = [
    data_folder / "chatgpt_india_simulated_sales_25000.csv",
    data_folder / "chatgpt_usa_simulated_sales_25000.csv"
]

for file in sales_files:
    print("\n" + "=" * 70)
    print("DATA QUALITY REPORT:", file.name)
    print("=" * 70)

    df = pd.read_csv(file)

    # 1. Dataset size
    print("\n1. Dataset size")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # 2. Missing values
    print("\n2. Missing values by column")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.any() else "No missing values found.")

    # 3. Duplicate records
    print("\n3. Duplicate checks")
    print("Duplicate full rows:", df.duplicated().sum())
    print("Duplicate transaction IDs:",
          df["transaction_id"].duplicated().sum())
    print("Duplicate customer IDs:", df["customer_id"].duplicated().sum())

    # 4. Data types
    print("\n4. Current data types")
    print(df.dtypes.to_string())

    # 5. Check dates without changing the original data
    print("\n5. Invalid transaction dates")
    dates = pd.to_datetime(df["transaction_date"], errors="coerce")
    print("Invalid dates:", dates.isna().sum())

    # 6. Check important numeric columns
    print("\n6. Numeric column checks")
    for column in [
        "list_price_local",
        "discount_amount_local",
        "net_revenue_local"
    ]:
        values = pd.to_numeric(df[column], errors="coerce")
        print(f"{column}: invalid numeric values = {values.isna().sum()}")

    # 7. Check business rules
    print("\n7. Business rule checks")
    print("Negative list prices:", (df["list_price_local"] < 0).sum())
    print("Negative discounts:", (df["discount_amount_local"] < 0).sum())
    print("Negative net revenue:", (df["net_revenue_local"] < 0).sum())

    print("Unexpected data_type values:",
          (~df["data_type"].eq("SIMULATED")).sum())

    print("Payment status values:")
    print(df["payment_status"].value_counts(dropna=False).to_string())

    print("\nSubscription plan values:")
    print(df["subscription_plan"].value_counts(dropna=False).to_string())
