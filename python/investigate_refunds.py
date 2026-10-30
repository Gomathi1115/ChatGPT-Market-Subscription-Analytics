
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

    # Count payment statuses
    print("\nPayment status counts:")
    print(df["payment_status"].value_counts())

    # Compare payment status with revenue sign
    print("\nPayment status vs revenue sign:")
    df["revenue_sign"] = df["net_revenue_local"].apply(
        lambda x: "Negative" if x < 0
        else "Zero" if x == 0
        else "Positive"
    )

    print(pd.crosstab(
        df["payment_status"],
        df["revenue_sign"]
    ))

    # Inspect refunded transactions
    refunds = df[df["payment_status"] == "Refunded"]

    print("\nRefunded transaction sample:")
    print(refunds[[
        "transaction_id",
        "payment_status",
        "subscription_event",
        "list_price_local",
        "discount_amount_local",
        "net_revenue_local"
    ]].head(5).to_string(index=False))
