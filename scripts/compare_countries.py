import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. Load and Combine all cleaned data
clean_files = [f for f in os.listdir('data') if f.endswith('_clean.csv')]
all_data = pd.concat([pd.read_csv(f"data/{f}") for f in clean_files])

print(f"Combined data from {len(clean_files)} countries.")

# 2. Comparison: Average Temperature by Country
plt.figure(figsize=(10, 6))
sns.boxplot(data=all_data, x='Country', y='T2M', palette='Set2')
plt.title('Temperature Distribution Comparison')
plt.ylabel('Temperature (°C)')
plt.savefig("notebooks/plots/country_temp_comparison.png")
plt.close()

# 3. Comparison: Total Rainfall by Country
# We group by Country and YEAR to get annual totals
annual_rain = all_data.groupby(['Country', 'YEAR'])['PRECTOTCORR'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=annual_rain, x='Country', y='PRECTOTCORR', ci='sd', palette='Blues')
plt.title('Average Annual Precipitation Comparison')
plt.ylabel('Total Annual Rainfall (mm)')
plt.savefig("notebooks/plots/country_rain_comparison.png")
plt.close()

# 4. Correlation Analysis (Cross-Country)
# How does Humidity (RH2M) relate to Temperature (T2M) across the region?
plt.figure(figsize=(10, 6))
sns.scatterplot(data=all_data.sample(2000), x='T2M', y='RH2M', hue='Country', alpha=0.5)
plt.title('Temperature vs Humidity Relationship')
plt.savefig("notebooks/plots/temp_vs_humidity_scatter.png")
plt.close()

print("Comparison plots saved to notebooks/plots/")