import pandas as pd
import numpy as np
import os
from scipy import stats

def clean_country_data(filename, country_name):
    # 1. Load Data
    path = f"data/{filename}"
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return
    
    df = pd.read_csv(path)
    print(f"\n--- Processing {country_name} ---")

    # 2. Add Country Column
    df["Country"] = country_name

    # 3. Replace NASA Sentinel Values (-999) with NaN
    df.replace(-999, np.nan, inplace=True)

    # 4. Date Parsing
    df['Date'] = pd.to_datetime(df["YEAR"] * 1000 + df["DOY"], format="%Y%j")
    df['Month'] = df['Date'].dt.month

    # 5. Handle Duplicates
    initial_len = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_len - len(df)} duplicate rows.")

    # 6. Missing Values Report
    missing_pct = (df.isna().sum() / len(df)) * 100
    cols_with_missing = missing_pct[missing_pct > 0]
    if not cols_with_missing.empty:
        print("Missing Values detected:")
        print(cols_with_missing)

    # 7. Outlier Detection (Z-Score > 3)
    weather_vars = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M']
    # Calculate Z-scores, skipping NaNs
    z_scores = np.abs(stats.zscore(df[weather_vars], nan_policy='omit'))
    outliers = (z_scores > 3).any(axis=1).sum()
    print(f"Identified {outliers} rows with outliers.")

    # 8. Final Cleaning: Forward-fill missing values
    df[weather_vars] = df[weather_vars].ffill()

    # 9. Export Cleaned CSV
    output_path = f"data/{country_name.lower()}_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully saved cleaned data to: {output_path}")

# List your 5 files here exactly as they are named in your data/ folder
countries = {
    "ethiopia.csv": "Ethiopia",
    "kenya.csv": "Kenya",
    "nigeria.csv": "Nigeria",
    "sudan.csv": "Sudan",
    "tanzania.csv": "Tanzania",
    # Add your other 4 countries here like this:
    # "kenya.csv": "Kenya",
}

for file, name in countries.items():
    clean_country_data(file, name)