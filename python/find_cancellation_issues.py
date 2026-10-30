
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

    # Cancellation event without a Yes flag
    issue_1 = df[
        (df["subscription_event"] == "Cancellation") &
        (df["is_cancelled"] != "Yes")
    ]

    # Yes flag on an event other than Cancellation
    issue_2 = df[
        (df["is_cancelled"] == "Yes") &
        (df["subscription_event"] != "Cancellation")
    ]

    print("Cancellation events not flagged Yes:", len(issue_1))
    print("Yes flags on non-cancellation events:", len(issue_2))

    print("\nSample of non-cancellation events flagged Yes:")
    print(issue_2[[
        "transaction_id",
        "customer_id",
        "subscription_event",
        "payment_status",
        "is_cancelled"
    ]].head(10).to_string(index=False))
