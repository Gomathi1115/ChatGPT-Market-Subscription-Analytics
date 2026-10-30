
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
clean_folder = project_path / "data" / "cleaned"
report_folder = project_path / "reports"
report_folder.mkdir(parents=True, exist_ok=True)

files = {
    "India": clean_folder / "chatgpt_india_simulated_sales_25000_cleaned.csv",
    "USA": clean_folder / "chatgpt_usa_simulated_sales_25000_cleaned.csv"
}

lines = [
    "# ChatGPT Market & Subscription Analytics",
    "",
    "Note: This report analyzes simulated transaction data,",
    "not actual OpenAI sales or customer records.",
    ""
]

for country, file in files.items():
    df = pd.read_csv(file)
    paid = df[df["payment_status"] == "Paid"]

    revenue_by_plan = paid.groupby("subscription_plan")[
        "net_revenue_local"
    ].sum()

    transaction_count_by_plan = paid.groupby(
        "subscription_plan"
    )["transaction_id"].count()

    top_revenue_plan = revenue_by_plan.idxmax()
    most_transactions_plan = transaction_count_by_plan.idxmax()

    lines.extend([
        f"## {country}",
        f"- Total transactions: {len(df):,}",
        f"- Successful transactions: {len(paid):,}",
        f"- Successful revenue (local currency): {paid['net_revenue_local'].sum():,.2f}",
        f"- Highest-revenue plan: {top_revenue_plan}",
        f"- Most successful transactions by plan: {most_transactions_plan}",
        ""
    ])

output_file = report_folder / "business_summary.md"
output_file.write_text("\n".join(lines), encoding="utf-8")

print("Business summary saved:", output_file)
print("\n".join(lines))
