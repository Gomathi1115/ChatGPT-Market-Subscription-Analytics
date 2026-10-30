
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

project_path = Path(r"D:\ChatGPT_Market_Analytics")
clean_folder = project_path / "data" / "cleaned"
output_folder = project_path / "reports" / "charts"
output_folder.mkdir(parents=True, exist_ok=True)

files = {
    "India": clean_folder / "chatgpt_india_simulated_sales_25000_cleaned.csv",
    "USA": clean_folder / "chatgpt_usa_simulated_sales_25000_cleaned.csv"
}

for country, file in files.items():
    df = pd.read_csv(file)
    paid = df[df["payment_status"] == "Paid"]

    revenue = (
        paid.groupby("subscription_plan")["net_revenue_local"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    revenue.plot(kind="bar")
    plt.title(f"{country}: Successful Revenue by Subscription Plan")
    plt.xlabel("Subscription Plan")
    plt.ylabel("Revenue (Local Currency)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_file = output_folder / f"{country.lower()}_plan_revenue.png"
    plt.savefig(output_file, dpi=150)
    plt.show()
    plt.close()

    print("Chart saved:", output_file)
