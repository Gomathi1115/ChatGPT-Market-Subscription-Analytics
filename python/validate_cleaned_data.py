
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
clean_folder = project_path / "data" / "cleaned"

files = [
    clean_folder / "chatgpt_india_simulated_sales_25000_cleaned.csv",
    clean_folder / "chatgpt_usa_simulated_sales_25000_cleaned.csv"
]

for file in files:
    df = pd.read_csv(file)

    print("\nCountry file:", file.name)
    print("Total rows:", len(df))
    print("Duplicate transaction IDs:",
          df["transaction_id"].duplicated().sum())
    print("Missing values:", df.isnull().sum().sum())
    print("Negative revenue rows:",
          (df["net_revenue_local"] < 0).sum())
    print("Failed payments:",
          (df["payment_status"] == "Failed").sum())
    print("Refunded payments:",
          (df["payment_status"] == "Refunded").sum())
    print("Cancellation mismatches:",
          df["cancellation_flag_mismatch"].astype(str)
          .str.lower().eq("true").sum())
