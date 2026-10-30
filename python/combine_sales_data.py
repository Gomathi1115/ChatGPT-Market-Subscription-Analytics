
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
clean_folder = project_path / "data" / "cleaned"

india_file = clean_folder / "chatgpt_india_simulated_sales_25000_cleaned.csv"
usa_file = clean_folder / "chatgpt_usa_simulated_sales_25000_cleaned.csv"

india = pd.read_csv(india_file)
usa = pd.read_csv(usa_file)

combined = pd.concat([india, usa], ignore_index=True)

output_file = clean_folder / "combined_sales_50000.csv"
combined.to_csv(output_file, index=False)

print("India rows:", len(india))
print("USA rows:", len(usa))
print("Combined rows:", len(combined))
print("Unique transaction IDs:", combined["transaction_id"].nunique())
print("Saved file:", output_file)
