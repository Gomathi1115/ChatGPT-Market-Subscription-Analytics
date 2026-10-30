
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
raw_folder = project_path / "data" / "raw"
clean_folder = project_path / "data" / "cleaned"

clean_folder.mkdir(parents=True, exist_ok=True)

files = [
    raw_folder / "chatgpt_india_simulated_sales_25000.csv",
    raw_folder / "chatgpt_usa_simulated_sales_25000.csv"
]

for file in files:
    df = pd.read_csv(file)

    # Convert date columns
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )
    df["transaction_month"] = pd.to_datetime(
        df["transaction_month"], format="%Y-%m", errors="coerce"
    )

    # Add a data-quality flag; do not overwrite the original flag
    df["cancellation_flag_mismatch"] = (
        (df["is_cancelled"] == "Yes") &
        (df["subscription_event"] != "Cancellation")
    )

    # Save a cleaned copy, preserving the raw data
    output_file = clean_folder / f"{file.stem}_cleaned.csv"
    df.to_csv(output_file, index=False, date_format="%Y-%m-%d")

    print("\nFile:", output_file.name)
    print("Rows preserved:", len(df))
    print("Missing transaction dates:", df["transaction_date"].isna().sum())
    print(
        "Cancellation flag mismatches:",
        int(df["cancellation_flag_mismatch"].sum())
    )
    print("Saved successfully:", output_file.exists())
