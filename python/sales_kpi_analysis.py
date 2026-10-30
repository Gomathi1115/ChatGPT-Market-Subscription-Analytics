
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

    # Successful payments only
    paid = df[df["payment_status"] == "Paid"].copy()

    total_transactions = len(df)
    successful_transactions = len(paid)
    failed_transactions = (df["payment_status"] == "Failed").sum()
    refunded_transactions = (df["payment_status"] == "Refunded").sum()

    successful_revenue = paid["net_revenue_local"].sum()
    average_paid_transaction = paid["net_revenue_local"].mean()

    print(f"\n--- {country} Sales KPIs ---")
    print("Total transactions:", total_transactions)
    print("Successful transactions:", successful_transactions)
    print("Failed transactions:", failed_transactions)
    print("Refunded transactions:", refunded_transactions)
    print("Successful revenue (local currency):",
          round(successful_revenue, 2))
    print("Average paid transaction value (local currency):",
          round(average_paid_transaction, 2))
