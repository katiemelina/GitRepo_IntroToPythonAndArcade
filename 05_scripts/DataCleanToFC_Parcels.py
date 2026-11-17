import os
import pandas as pd
import arcpy

arcpy.AddMessage("Starting Parcels Clean + Join Tool...")

# Parameters (set up in this order in the tool dialog)
input_csv = arcpy.GetParameterAsText(0)       # raw parcels csv - file
output_folder = arcpy.GetParameterAsText(1)   # where the cleaned csv goes - folder
output_filename = arcpy.GetParameterAsText(2) # cleaned csv name - string
parcel_shp = arcpy.GetParameterAsText(3)      # parcels shapefile - feature class
output_fc = arcpy.GetParameterAsText(4)       # output polygons (use a geodatabase feature class); set direction as output

output_csv = os.path.join(output_folder, output_filename)

# Load (HANDLE as text so it can't become a number)
df = pd.read_csv(input_csv, dtype={'HANDLE': str})
arcpy.AddMessage(f"Loaded raw data with shape: {df.shape}")

# Keep only the columns we want (for this data set, these are in the shapefile)
columns_to_keep = [
    'HANDLE', 'SITEADDR', 'OWNERNAME', 'ZONING1', 'LANDUSE1',
    'ASMTLAND', 'ASMTIMPROV', 'ASMTTOTAL', 'NUMBLDGS', 'LANDAREA',
    'WARD', 'NBRHD', 'ZIP', 'IMPROVED', 'ASMT_PER_ACRE'
]
# New columns for the join to show (calculated from csv columns the polygons don't have)
# IMPROVED: "Improved" if the assessed value of improvements is above 0
df['IMPROVED'] = (df['ASMTIMPROV'] > 0).map({True: 'Improved', False: 'Unimproved'})

# ASMT_PER_ACRE: total assessed value / acres (LANDAREA assumed square feet; 0 = not recorded)
acres = df['LANDAREA'].where(df['LANDAREA'] > 0) / 43560
df['ASMT_PER_ACRE'] = df['ASMTTOTAL'] / acres

# Add the new columns to the existing columns list
df = df[columns_to_keep + ['IMPROVED', 'ASMT_PER_ACRE']].copy()

# Check HANDLE
df['HANDLE'] = df['HANDLE'].str.strip()
n_missing = df['HANDLE'].isna().sum()
if n_missing > 0:
    arcpy.AddMessage(f"Dropping {n_missing} rows with no HANDLE")
df_clean = df.dropna(subset=['HANDLE']).copy()

dupes = df_clean[df_clean['HANDLE'].duplicated(keep=False)]['HANDLE'].unique().tolist()
if dupes:
    arcpy.AddMessage(f"WARNING: repeated HANDLEs (only the first row is used in the join): {dupes}")

# Sort and export
df_clean = df_clean.sort_values(by='HANDLE')
os.makedirs(output_folder, exist_ok=True)
df_clean.to_csv(output_csv, index=False)
arcpy.AddMessage(f"Cleaned data saved to: {output_csv} ({len(df_clean)} rows)")

# Copy the parcels so the original is untouched
arcpy.management.CopyFeatures(parcel_shp, output_fc)

# Add a field for each csv column; fields the polygons already have are reused and overwritten
existing = [f.name.upper() for f in arcpy.ListFields(output_fc)]
new_fields = []
for col in df_clean.columns:
    if col == 'HANDLE':
        continue
    if col.upper() in existing:
        arcpy.AddMessage(f"'{col}' already exists in the parcels: its values will be overwritten from the csv")
    elif pd.api.types.is_numeric_dtype(df_clean[col]):
        arcpy.management.AddField(output_fc, col, "DOUBLE")
    else:
        arcpy.management.AddField(output_fc, col, "TEXT", field_length=255)
    new_fields.append(col)

# Fill the new fields, matching each polygon to its csv row by HANDLE
def make_key(v):
    # make HANDLE comparable as text (handles 123.0 vs 123, stray spaces)
    if v is None:
        return None
    s = str(v).strip()
    return s[:-2] if s.endswith('.0') else s

records = df_clean.drop_duplicates(subset='HANDLE', keep='first').set_index('HANDLE').to_dict('index')
matched_keys = set()
matched = 0
unmatched = 0

with arcpy.da.UpdateCursor(output_fc, ['HANDLE'] + new_fields) as cursor:
    for row in cursor:
        k = make_key(row[0])
        rec = records.get(k)
        if rec is None:
            unmatched += 1
            continue
        for i, name in enumerate(new_fields, start=1):
            val = rec[name]
            if pd.isna(val):
                row[i] = None
            else:
                row[i] = val.item() if hasattr(val, 'item') else val
        cursor.updateRow(row)
        matched_keys.add(k)
        matched += 1

# Report the match
csv_only = len(set(records) - matched_keys)
arcpy.AddMessage(f"Polygons with a csv match: {matched}")
arcpy.AddMessage(f"Polygons with NO csv match: {unmatched}")
arcpy.AddMessage(f"csv rows that matched no polygon: {csv_only}")
arcpy.AddMessage(f"Success! Joined polygons saved to: {output_fc}")