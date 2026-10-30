
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
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    print("\n" + "=" * 60)
    print("COUNTRY:", df["country"].iloc[0])
    print("=" * 60)

    # Count unique customers and repeat customers
    customer_counts = df["customer_id"].value_counts()

    print("Unique customers:", df["customer_id"].nunique())
    print("Customers with multiple transactions:",
          (customer_counts > 1).sum())
    print("Maximum transactions for one customer:",
          customer_counts.max())

    # Inspect customers marked as cancelled
    cancelled_customers = df.loc[
        df["is_cancelled"] == "Yes", "customer_id"
    ].unique()

    history = df[df["customer_id"].isin(cancelled_customers)].sort_values(
        ["customer_id", "transaction_date"]
    )

    print("\nSample transaction history for customers with cancellation flags:")
    print(history[[
        "customer_id",
        "transaction_date",
        "subscription_event",
        "payment_status",
        "is_cancelled"
    ]].head(20).to_string(index=False))
