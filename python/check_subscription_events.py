
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

    print("\nSubscription event values:")
    print(df["subscription_event"].value_counts(dropna=False))

    print("\nPayment status by subscription event:")
    print(pd.crosstab(
        df["subscription_event"],
        df["payment_status"],
        margins=True
    ))

    print("\nCancellation flag by subscription event:")
    print(pd.crosstab(
        df["subscription_event"],
        df["is_cancelled"],
        margins=True
    ))
