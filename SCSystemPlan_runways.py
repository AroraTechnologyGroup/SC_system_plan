import arcpy
from arcpy import da, env
from collections import Counter
env.overwriteOutput = 1

sitelist = []
with da.SearchCursor('PrimAirports_Runway', ["SiteNumber"]) as cursor:
    for row in cursor:
        sitelist.append(row[0])

cnt = Counter(sitelist)
rem = []
for k, v in cnt.items():
    if v == 1:
        rem.append(k)
for k in rem:
    del cnt[k]

sitelist = list(set(cnt.elements()))

for x in sitelist:
    lengths = []
    with da.SearchCursor('PrimAirports_Runway', ["MaxRunwayLength"], "SiteNumber = '{}'".format(x)) as cursor:
        for row in cursor:
            value = row[0]
            if value is None:
                value = 0
            lengths.append(float(value))
    max_length = float(max(lengths))
    print ("{} is the largest of {}".format(max_length, lengths))
    number_of_runways = 0
    with da.UpdateCursor('PrimAirports_Runway', ["MaxRunwayLength"], "SiteNumber = '{}'".format(x)) as cursor:
        for row in cursor:
            value = row[0]
            if value is None:
                value = 0.0
            value = float(value)
            print("value={} ; max_length={}".format(value, max_length))
            if value != max_length:
                cursor.deleteRow()
                print("row deleted, {} is shorter than {}".format(value, max_length))

            if value == max_length:
                if not number_of_runways:
                    number_of_runways += 1
                else:
                    cursor.deleteRow()
                    print("deleted runway length of {}, identical to current longest of {}".format(value, max_length))







