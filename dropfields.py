import arcpy
from arcpy import da

fields = arcpy.ListFields('Pilot_Cert')
fields = [f.name for f in fields]
drop = []
for name in fields:
    populated = 0
    with da.SearchCursor('Pilot_Cert', ["{}".format(name)]) as cursor:
        for row in cursor:
            if row[0] is not None and str(row[0]).strip() != "":
                populated += 1
            else:
                pass
    if not populated:
        drop.append(name)
