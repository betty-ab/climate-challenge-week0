import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create a folder to save your plots if it doesn't exist
os.makedirs("notebooks/plots", exist_ok=True)

def create_visuals(country_clean_csv, country_name):
    # Load the cleaned data
    df = pd.read_csv(f"data/{country_clean_csv}")
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"Generating plots for {country_name}...")

    # 1. Time Series: Monthly Average Temperature (T2M)
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='T2M', color='teal')
    plt.title(f'Temperature Trend (2015-2026) - {country_name}')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f"notebooks/plots/{country_name.lower()}_temp_trend.png")
    plt.close()

    # 2. Precipitation Bar Chart (Monthly Totals)
    # Grouping by year and month to see seasonality clearly
    monthly_precip = df.groupby(['YEAR', 'Month'])['PRECTOTCORR'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=monthly_precip.tail(24), x='Month', y='PRECTOTCORR', color='blue')
    plt.title(f'Recent Monthly Precipitation - {country_name} (Last 2 Years)')
    plt.ylabel('Total Precipitation (mm)')
    plt.savefig(f"notebooks/plots/{country_name.lower()}_precip_bar.png")
    plt.close()

    # 3. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    weather_vars = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M']
    corr = df[weather_vars].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(f'Weather Correlation Matrix - {country_name}')
    plt.savefig(f"notebooks/plots/{country_name.lower()}_heatmap.png")
    plt.close()

# List the cleaned files you generated in the previous step
clean_files = {
    "ethiopia_clean.csv": "Ethiopia",
    "kenya_clean.csv": "Kenya",
    "nigeria_clean.csv": "Nigeria",
    "sudan_clean.csv": "Sudan",
    "tanzania_clean.csv": "Tanzania",
    # "kenya_clean.csv": "Kenya",
}

for file, name in clean_files.items():
    create_visuals(file, name)

print("\nDone! Check the 'notebooks/plots/' folder for your images.")