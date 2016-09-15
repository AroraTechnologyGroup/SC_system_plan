import arcpy
from arcpy import da, env
from collections import Counter
env.overwriteOutput = 1

ingdb = r"C:\Users\rhughes\Documents\ArcGIS\Projects\SCAEC Service Area Analysis\SCAEC Service Area Analysis.gdb"
env.workspace = ingdb

pilot_table = arcpy.ListTables("Pilot_Basic_Regional")[0]
pilot_cert = arcpy.ListTables("Pilot_Cert")[0]
non_pilot_table = arcpy.ListTables("NonPilot_Basic_Regional")[0]
non_pilot_cert = arcpy.ListTables("NonPilot_Cert")[0]

for x in [pilot_table, pilot_cert, non_pilot_table, non_pilot_cert]:
    fields = arcpy.ListFields(x)
    field_names = [f.name for f in fields]
    drop = []
    for name in field_names:
        populated = 0
        with da.SearchCursor(x, ["{}".format(name)]) as cursor:
            for row in cursor:
                if row[0] is not None and str(row[0]).strip() != "":
                    populated += 1
                else:
                    pass
        if not populated:
            drop.append(name)

    print("{} can drop fields {}".format(x, drop))
