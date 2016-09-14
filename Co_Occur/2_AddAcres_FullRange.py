import arcpy
import os

intable = 'C:\WorkSpace\MasterOverlap\Acres.gdb\Acres_20151207'
folderDict = 'J:\Workspace\ESA_Species\ForCoOccur\Dict\FullRange_Acres.csv'



def fcs_in_workspace(workspace):
    arcpy.env.workspace = workspace
    for fc in arcpy.ListFeatureClasses():
        yield (fc)
    for ws in arcpy.ListWorkspaces():
        for fc in fcs_in_workspace(ws):
            yield fc


with open(folderDict, 'rU') as inputFile:
    for line in inputFile:
        line = line.split(',')
        finalGDB = str(line[0])
        finalGDB = finalGDB.strip('\n')
        print finalGDB

        for fc in fcs_in_workspace(finalGDB):
            # print fc
            CHcheck = fc.split("_")
            CHcheck = CHcheck[0]
            # print CHcheck
            if CHcheck == 'CH':
                col = "Full"

                field = col + "_" + CHcheck
                # print field

                acres_dict = {}
                entlist = []

                infc = finalGDB + os.sep + fc
                with arcpy.da.SearchCursor(infc, ["EntityID", "Acres"]) as cursor:
                    for row in cursor:
                        ent = str(row[0])
                        # print row[1]
                        acres_dict[ent] = row[1]
                        entlist.append(str(ent))
                    del row, cursor

                with arcpy.da.UpdateCursor(intable, ["EntityID", field]) as cursor:
                    # print entlist

                    for row in cursor:
                        ent = str(row[0])
                        if ent in entlist:
                            print field
                            print ent
                            acres = acres_dict[ent]
                            row[1] = acres
                            print acres
                            cursor.updateRow(row)
                        else:
                            # print ent
                            # print 'not in list'
                            continue
                    del row, cursor

            else:

                col = "Full"

                field = col + "_R"
                # print field

                acres_dict = {}
                entlist = []

                infc = finalGDB + os.sep + fc
                with arcpy.da.SearchCursor(infc, ["EntityID", "Acres"]) as cursor:
                    for row in cursor:
                        ent = str(row[0])
                        acres_dict[ent] = row[1]
                        entlist.append(str(ent))
                    del row, cursor

                with arcpy.da.UpdateCursor(intable, ["EntityID", field]) as cursor:
                    # print entlist

                    for row in cursor:
                        ent = str(row[0])
                        # print ent
                        if ent in entlist:
                            print field
                            print ent
                            acres = acres_dict[ent]
                            row[1] = acres
                            print acres
                            cursor.updateRow(row)
                        else:
                            # print 'not in list'
                            # print ent
                            continue
                    del row, cursor
