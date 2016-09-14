import arcpy
from arcpy import da

page_names = []

with da.SearchCursor('Demo Service Areas', ["Name"]) as cursor:
    for row in cursor:
        page_names.append(row[0])

page_names = list(set(page_names))

arcpy.SelectLayerByAttribute_management('Demo Service Areas', 'CLEAR_SELECTION')
arcpy.SelectLayerByAttribute_management('Pilot and Mechanic Locations\\Pilot Locations', 'CLEAR_SELECTION')
arcpy.SelectLayerByAttribute_management('Pilot and Mechanic Locations\\Mechanic Locations', 'CLEAR_SELECTION')
service = arcpy.MakeFeatureLayer_management('Demo Service Areas', "service_area_layer")
layer = arcpy.MakeFeatureLayer_management('Pilot and Mechanic Locations\\Pilot Locations', "temp_layer")
layer2 = arcpy.MakeFeatureLayer_management('Pilot and Mechanic Locations\\Mechanic Locations', "temp_layer2")

try:
    for airport in page_names:

        arcpy.SelectLayerByAttribute_management(service, 'NEW_SELECTION', "Name = '{}'".format(airport))

        if int(arcpy.GetCount_management(service).getOutput(0)) != 1:
            raise Exception

        for x in [layer, layer2]:
            before_cnt = int(arcpy.GetCount_management(x).getOutput(0))
            arcpy.SelectLayerByLocation_management(x, 'WITHIN', service, "", 'NEW_SELECTION')
            after_cnt = int(arcpy.GetCount_management(x).getOutput(0))

            if after_cnt >= before_cnt:
                raise Exception

            with da.UpdateCursor(x, ["PageName"]) as cursor:
                for row in cursor:
                    new_row = [airport]
                    cursor.updateRow(new_row)
            arcpy.SelectLayerByAttribute_management(x, 'CLEAR_SELECTION')

        arcpy.SelectLayerByAttribute_management(service, 'CLEAR_SELECTION')


except:
    print(arcpy.GetMessages())

for x in [layer, layer2, service]:
    del x

for x in ["temp_layer", "temp_layer2", "service_area_layer"]:
    if arcpy.Exists(x):
        arcpy.Delete_management(x)

