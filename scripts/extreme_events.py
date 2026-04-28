import pandas as pd
import os

clean_files = [f for f in os.listdir('data') if f.endswith('_clean.csv')]
summary_list = []

for f in clean_files:
    df = pd.read_csv(f"data/{f}")
    country = df['Country'].iloc[0]
    
    # Count Heatwaves: Days > 35°C
    heat_days = (df['T2M_MAX'] > 35).sum()
    
    # Count Drought Days: Precipitation < 1mm
    drought_days = (df['PRECTOTCORR'] < 1).sum()
    
    summary_list.append({
        "Country": country,
        "Extreme Heat Days": heat_days,
        "Dry Days": drought_days,
        "Avg Temp": df['T2M'].mean(),
        "Rain Volatility (StdDev)": df['PRECTOTCORR'].std()
    })

ranking_df = pd.DataFrame(summary_list)
ranking_df = ranking_df.sort_values(by="Extreme Heat Days", ascending=False)
print("\n--- COP32 Climate Vulnerability Ranking Data ---")
print(ranking_df)
ranking_df.to_csv("vulnerability_ranking.csv", index=False)