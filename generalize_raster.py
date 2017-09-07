# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Generalize Flood Extent
# Created on: 2017-09-07 17:50:53.00000
# by Firman Hadi (firmanhadi@me.com, www.sigro.web.id)
# Description: 
# Simple tool to generalize raster file from change detection
# analysis. It combines generalization tools such as
# Majority Filter, Boundary Clean, Region group,
# Set Null and Nibble from ArcGIS Geoprocessing Tools
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

Folder = "C:\\Temp"
GDBName = "flood.gdb"
GDB = Folder + "\\" + GDBName

if arcpy.Exists(GDB):
	arcpy.Delete_management(GDB)
arcpy.CreateFileGDB_management(Folder, GDBName)

#Setting Workspace
arcpy.env.workspace = GDB

#Input file for flood image
flood_image = arcpy.GetParameterAsText(0)

# Local variables:
Majorit_tif = GDB +"\\" + "Majorit_tif"
Boundar_Majo = GDB + "\\" + "Boundar_Majo"
RegionG_Boun = GDB + "\\" + "RegionG_Boun"
SetNull_Reg = GDB + "\\" + "SetNull_Reg"
generalized_flood_extent = GDB + "\\" + "generalized_flood_extent"
generalized_flood_shp = Folder + "\\" + "generalized_flood.shp"
Input_false_raster_or_constant_value = "0"


# Process: Majority Filter
arcpy.gp.MajorityFilter_sa(flood_image, Majorit_tif, "FOUR", "MAJORITY")

# Process: Boundary Clean
arcpy.gp.BoundaryClean_sa(Majorit_tif, Boundar_Majo, "NO_SORT", "TWO_WAY")

# Process: Region Group
arcpy.gp.RegionGroup_sa(Boundar_Majo, RegionG_Boun, "FOUR", "WITHIN", "ADD_LINK", "")

# Process: Set Null
arcpy.gp.SetNull_sa(RegionG_Boun, Input_false_raster_or_constant_value, SetNull_Reg, "\"COUNT\" < 50")

# Process: Nibble
arcpy.gp.Nibble_sa(Boundar_Majo, SetNull_Reg, generalized_flood_extent, "ALL_VALUES")

# Process: Raster to Polygon
arcpy.RasterToPolygon_conversion(generalized_flood_extent, generalized_flood_shp, "SIMPLIFY", "VALUE")

# Process: Raster To Other Format (multiple)
arcpy.RasterToOtherFormat_conversion(generalized_flood_extent, Folder, "TIFF")

