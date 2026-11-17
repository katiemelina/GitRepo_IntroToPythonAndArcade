import os
import pandas as pd
import arcpy

arcpy.AddMessage("Starting Clean + Make Points Tool...")

# Parameters from the ArcGIS Pro tool dialog (set up in this order)
input_csv = arcpy.GetParameterAsText(0)       # raw csv - file
output_folder = arcpy.GetParameterAsText(1)   # where the cleaned csv goes - folder
output_filename = arcpy.GetParameterAsText(2) # cleaned csv name, e.g. milkweed_clean.csv - string
output_fc = arcpy.GetParameterAsText(3)       # output point feature class - output

output_csv = os.path.join(output_folder, output_filename)

# Load the csv
df = pd.read_csv(input_csv)
arcpy.AddMessage(f"Loaded raw data with shape: {df.shape}")

# Planting date: parse, then fill blanks with a MADE-UP placeholder (demo only)
df['planting_dt'] = pd.to_datetime(df['PLANTINGDATE'], errors='coerce')
df['planting_dt'] = df['planting_dt'].fillna(pd.Timestamp('2026-03-15'))

# Keep only certain columns
columns_to_keep = [
    'RECORDNO', 'HANDLE', 'SITEADDRESS', 'CITY', 'NEIGHBORHOOD',
    'WARD', 'ZIPCODE', 'MILKWEED', 'NECTARSOURCE', 'DESCRIPTION',
    'planting_dt', 'POINTX', 'POINTY'
]
df = df[columns_to_keep].copy()

# Report rows with no coordinates, then drop them
missing = df[df['POINTX'].isna() | df['POINTY'].isna()]
if len(missing) > 0:
    arcpy.AddMessage(f"Rows missing coordinates (RECORDNO): {missing['RECORDNO'].tolist()}")
df_clean = df.dropna(subset=['POINTX', 'POINTY']).copy()

# Standardize city capitalization
df_clean['CITY'] = df_clean['CITY'].str.title()

# Sort
df_clean = df_clean.sort_values(by='RECORDNO', ascending=True)

# Export the cleaned csv
os.makedirs(output_folder, exist_ok=True)
df_clean.to_csv(output_csv, index=False)
arcpy.AddMessage(f"Cleaned data saved to: {output_csv}")
arcpy.AddMessage(f"Final row count: {len(df_clean)}")

# Convert to points. These are NOT lat/long.
# 102696 = NAD 1983 StatePlane MO
x_field = "POINTX"
y_field = "POINTY"
spatial_ref = arcpy.SpatialReference(102696)

arcpy.management.XYTableToPoint(
    in_table=output_csv,
    out_feature_class=output_fc,
    x_field=x_field,
    y_field=y_field,
    coordinate_system=spatial_ref
)

arcpy.AddMessage(f"Successfully created point feature class: {output_fc}")


