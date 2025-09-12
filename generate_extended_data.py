"""
Generate extended synthetic data (2024-2025) and merge with existing dataset.

Usage::
    python generate_extended_data.py

This will create/overwrite:
    data/hackathon_data_extended.csv  (only new period)
    data/hackathon_data_full.csv       (2022-2025 combined)

The script guarantees date uniqueness and logs basic statistics.
"""
import os
import pandas as pd
from datetime import datetime

from src.data_preparation import DataPreparation

DATA_DIR = "data"
EXISTING = os.path.join(DATA_DIR, "hackathon_data.csv")
EXTENDED = os.path.join(DATA_DIR, "hackathon_data_extended.csv")
FULL = os.path.join(DATA_DIR, "hackathon_data_full.csv")

START_DATE = "2024-01-01"
DAYS = 730  # 2 years


def main():
    dp = DataPreparation()

    # 1. Generate new synthetic data for 2024-2025
    new_df = dp.generate_sample_data(start_date=START_DATE, days=DAYS)
    new_df.to_csv(EXTENDED, index=False)
    print(f"💾 Saved extended period to {EXTENDED} ({len(new_df)} rows)")

    # 2. Load existing dataset
    if not os.path.exists(EXISTING):
        raise FileNotFoundError(f"Existing dataset not found: {EXISTING}")
    orig_df = pd.read_csv(EXISTING)

    # 3. Merge, ensuring uniqueness by 'datum'
    combined = pd.concat([orig_df, new_df], ignore_index=True)
    combined.drop_duplicates(subset=["datum"], keep="first", inplace=True)
    combined.sort_values("datum", inplace=True)
    combined.to_csv(FULL, index=False)
    print(f"💾 Saved full dataset to {FULL} ({len(combined)} rows)")

    # 4. Quick sanity stats
    print("📊 Date range:", combined['datum'].min(), "→", combined['datum'].max())
    print("📊 Rows:", len(combined))


if __name__ == "__main__":
    main()
