import arcpy

arcpy.AddMessage("Starting Point Creation Tool...")

# 1. Get parameters from the ArcGIS Pro tool dialog box
input_csv = arcpy.GetParameterAsText(0)
output_fc = arcpy.GetParameterAsText(1)

# 2. Define coordinate fields and spatial reference (WGS 1984)
x_field = "longitude"
y_field = "latitude"
spatial_ref = arcpy.SpatialReference(4326)

# 3. Convert tabular coordinates into a spatial point feature class
arcpy.management.XYTableToPoint(
    in_table=input_csv,
    out_feature_class=output_fc,
    x_field=x_field,
    y_field=y_field,
    coordinate_system=spatial_ref
)

arcpy.AddMessage(f"Successfully created point feature class: {output_fc}")