
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
data_folder = project_path / "data" / "raw"

files = [
    data_folder / "chatgpt_india_simulated_sales_25000.csv",
    data_folder / "chatgpt_usa_simulated_sales_25000.csv"
]

for file in files:
    df = pd.read_csv(file)

    print("\n" + "=" * 60)
    print("COUNTRY:", df["country"].iloc[0])
    print("=" * 60)

    cancelled = df[df["is_cancelled"] == "Yes"]

    print("\nCancelled-flag row count:", len(cancelled))
    print("\nSubscription events among cancelled-flag rows:")
    print(cancelled["subscription_event"].value_counts())

    print("\nPayment statuses among cancelled-flag rows:")
    print(cancelled["payment_status"].value_counts())

    print("\nSample cancelled-flag records:")
    print(cancelled[[
        "transaction_id",
        "customer_id",
        "subscription_event",
        "payment_status",
        "is_cancelled",
        "transaction_date"
    ]].head(10).to_string(index=False))
