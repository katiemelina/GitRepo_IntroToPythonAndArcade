import os
import pandas as pd
import arcpy

arcpy.AddMessage("Starting Data Cleaning Tool...")

# Get parameters from the ArcGIS Pro Tool dialog box
input_csv = arcpy.GetParameterAsText(0)
output_folder = arcpy.GetParameterAsText(1)
output_filename = arcpy.GetParameterAsText(2)

# Combine folder and filename safely using os.path.join
output_csv = os.path.join(output_folder, output_filename)

# Load the dataset
df = pd.read_csv(input_csv)
arcpy.AddMessage(f"Loaded raw data with shape: {df.shape}")

# Parse dates and create a calculated year column
df['date_dt'] = pd.to_datetime(df['observed_on'], errors='coerce')
df['obs_year'] = df['date_dt'].dt.year

# Filter down to essential columns
columns_to_keep = [
    'id', 
    'date_dt', 
    'time_zone', 
    'latitude', 
    'longitude', 
    'scientific_name', 
    'common_name',
    'obs_year'
]
df = df[columns_to_keep].copy()

# Clean data (drop rows missing spatial coordinates, standardize text)
df_clean = df.dropna(subset=['latitude', 'longitude']).copy()
df_clean['common_name'] = df_clean['common_name'].str.title()

# Sort chronologically
df_clean = df_clean.sort_values(by='date_dt', ascending=True)

# Ensure output directory exists and export
os.makedirs(output_folder, exist_ok=True)
df_clean.to_csv(output_csv, index=False)

arcpy.AddMessage(f"Success! Cleaned data saved to: {output_csv}")
arcpy.AddMessage(f"Final row count: {len(df_clean)}")