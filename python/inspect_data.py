
from pathlib import Path
import pandas as pd

project_path = Path(r"D:\ChatGPT_Market_Analytics")
data_folder = project_path / "data" / "raw"

csv_files = list(data_folder.glob("*.csv"))

public_folder = data_folder / "public_release_csv"
if public_folder.exists():
    csv_files.extend(public_folder.rglob("*.csv"))

if not csv_files:
    print("No CSV files found. Check your folder paths.")
else:
    for file in csv_files:
        print("\n" + "=" * 60)
        print("FILE:", file.name)
        print("=" * 60)

        try:
            df = pd.read_csv(file, nrows=5)

            print("\nColumn names:")
            print(df.columns.tolist())

            print("\nFirst 5 rows:")
            print(df.to_string(index=False))

            print("\nNumber of columns:", len(df.columns))

        except Exception as error:
            print("Error reading file:", error)
