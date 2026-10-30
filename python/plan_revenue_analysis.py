
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
clean_folder = project_path / "data" / "cleaned"

files = {
    "India": clean_folder / "chatgpt_india_simulated_sales_25000_cleaned.csv",
    "USA": clean_folder / "chatgpt_usa_simulated_sales_25000_cleaned.csv"
}

for country, file in files.items():
    df = pd.read_csv(file)

    # Keep successful payments only
    paid = df[df["payment_status"] == "Paid"].copy()

    # Summarize revenue and transactions by plan
    summary = (
        paid.groupby("subscription_plan")
        .agg(
            successful_transactions=("transaction_id", "count"),
            total_revenue=("net_revenue_local", "sum"),
            average_transaction_value=("net_revenue_local", "mean")
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    print(f"\n--- {country}: Revenue by Subscription Plan ---")
    print(summary.round(2).to_string(index=False))
