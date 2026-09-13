import pandas as pd

# Step 1: Load the dataset
df = pd.read_csv("Minkw.csv")  # Replace with your actual filename

# Step 2: Clean column names
df.columns = df.columns.str.strip()

# Step 3: Convert 'minute' to datetime
df['minute'] = pd.to_datetime(df['minute'], errors='coerce')

# Step 4: Drop rows with invalid or missing datetimes
df = df.dropna(subset=['minute'])

# Step 5: Ensure 'power' column is numeric
df['power'] = pd.to_numeric(df['power'], errors='coerce')

# Step 6: Drop rows with missing or negative power values
df = df.dropna(subset=['power'])
df = df[df['power'] >= 0]

# Optional: remove extremely high values if needed (e.g., >100 kW)
df = df[df['power'] <= 100]

# Step 7: Set datetime index for resampling
df.set_index('minute', inplace=True)

# Step 8: Resample data hourly and convert kW to kWh (since it's minute-level)
df_hourly = df.resample('H').sum() * (1 / 60)

# Step 9: Prepare final output
df_hourly.reset_index(inplace=True)
df_hourly.columns = ['hour', 'kWh_generated']

# Step 10: Export to CSV
df_hourly.to_csv("hourly_output_clean.csv", index=False)

print("✅ Done! Output saved as 'hourly_output_clean.csv'")
