import os
import datetime
import arcpy
import pandas as pd
import sys

# Tile: Archives species files for species that have been removed from the ESA list or overlap analysis.  The reason the
# species is removed from the overlap analysis is appended to the beginning of the file name and the date of the archive
# is appended to the end.  A csv is outputs to track why a files was archived. The files to be removed are identified by
# comparing the previous master species list to the current one.

# compares new master list to old master and archives any species that has been removed.  User identifies reason for
# removal

#TODO Make the archive of the qualitative species dynamic
# User input variable
# input tables

masterlist_old = 'C:\Users\JConno02\OneDrive - Environmental Protection Agency (EPA)\Documents_C_drive\Projects\ESA' \
             '\_ExternalDrive\_CurrentSupportingTables\MasterLists\MasterListESA_Feb2017_20180109.csv'
masterlist_current = 'C:\Users\JConno02\OneDrive - Environmental Protection Agency (EPA)\Documents_C_drive\Projects\ESA' \
                 '\_ExternalDrive\_CurrentSupportingTables\MasterLists\MasterListESA_Feb2017_20180109_dropped_QualSpeciesCheck.csv'



# Reasons = Qual_, Delisted_, Extinct_,UninhabIsland_, PosExtinct_, CaveDweller_, DraftBEOther_,MostlyOutsideUS_,
# CaptivityOnly_, QualOther_
reason_removed = 'QualOther_'  # Prefix is appended to the beginning of the file name

today = datetime.datetime.today()
archive_date = today.strftime('%Y%m%d')

# in spatial library

infolder = 'C:\Users\JConno02\One_Drive_fail\Documents_C_drive\Projects\ESA\_ExternalDrive\_CurrentSpeciesSpatialFiles' \
           '\SpatialLibrary\Generalized files\CriticalHabitat'
# archive location
archivefolder = 'C:\Users\JConno02\One_Drive_fail\Documents_C_drive\Projects\ESA\_ExternalDrive' \
                '\_CurrentSpeciesSpatialFiles\SpatialLibrary\Generalized files\CriticalHabitat\Archived'

infolder = 'C:\Users\JConno02\One_Drive_fail\Documents_C_drive\Projects\ESA\_ExternalDrive\_CurrentSpeciesSpatialFiles' \
           '\SpatialLibrary\Generalized files\Range'
# archive location
archivefolder = 'C:\Users\JConno02\One_Drive_fail\Documents_C_drive\Projects\ESA\_ExternalDrive' \
                '\_CurrentSpeciesSpatialFiles\SpatialLibrary\Generalized files\Range\ArchivedRange'
# out table of all files that were archived
out_csv = archivefolder + os.sep + 'ArchivedSpecies_'+ reason_removed + archive_date + '.csv'
skipgroup = []

# #########Functions
# Create a new GDB
def create_gdb(out_folder, out_name, out_path):
    if not arcpy.Exists(out_path):
        arcpy.CreateFileGDB_management(out_folder, out_name, "CURRENT")
        print 'Created GDB {0}'.format(out_name)


# extract the info needed from master
def extract_info_master(master_list_current, master_list_old):
    df_old = pd.read_csv(master_list_old)
    df_old['EntityID'] = df_old['EntityID'].astype(str)

    df_new = pd.read_csv(master_list_current)
    df_new['EntityID'] = df_new['EntityID'].astype(str)
    filter_entids = df_new["EntityID"].tolist()

    # extract species found in old list but not new
    df_remove = df_old[df_old['EntityID'].isin(filter_entids) == False]
    print (df_remove)

    # prompt user to decide if the script should continue with archive, this will remove spatial file from active
    # spatial library and move it to the archived library

    qa_answer = True
    poss_answers = ['Yes', 'No']
    while qa_answer:
        user_input = raw_input('Would you like to continue with the archive? Yes or No ')
        if user_input not in poss_answers:
            print 'This is not a valid answswer'
        else:
            break
    if user_input == 'Yes':
        proceed_archive = True
        df_remove.to_csv(out_csv)
    else:
        print 'Script will end'
        sys.exit()

    dropped_species = df_remove["EntityID"].tolist()
    group_df = df_remove['Group']
    unq_groups = group_df.drop_duplicates()
    group_list = sorted(unq_groups.tolist())

    return dropped_species, group_list, proceed_archive


# loops through fcs in spatial library and extract location of file that needs to be archived
# stores information in dictionary entid as key
def find_archive_files(group_list, in_folder, skip_group, archive_list):
    location_dict = {}
    for group in group_list:
        if group in skip_group:
            continue
        print "\nWorking on {0}".format(group)
        group_gdb = in_folder + os.sep + str(group) + '.gdb'

        arcpy.env.workspace = group_gdb
        fclist = arcpy.ListFeatureClasses()

        for fc in fclist:

            ent_id = fc.split('_')
            entid = str(ent_id[1])

            if entid in archive_list:
                print entid

                if location_dict.get(entid) is None:

                    location_dict[entid] = [(group_gdb + os.sep + fc)]
                else:
                    locationlist = location_dict[entid]
                    locationlist.append((group_gdb + os.sep + fc))
    return location_dict


# use dictionaries from functions above function to determine which file is older and then archives is with the current
# file's date at the end of it
def archive_dup_files(location_dict, archive_folder, archive_list, archived_date):
    count = len(archive_list)
    for entid in archive_list:
        try:
            archive_file_list = location_dict[entid]
            for archive_fc in archive_file_list:
                path, archive_file_name = os.path.split(archive_fc)
                in_folder, group_gdb = os.path.split(path)
                archived_gdb = archive_folder + os.sep + group_gdb
                # creates archive gdb if it does not exist
                if not arcpy.Exists(archived_gdb):
                    create_gdb(archivefolder, group_gdb, archived_gdb)
                out_fc_archive = archived_gdb + os.sep + reason_removed+ archive_file_name + "_" + archived_date
                if not arcpy.Exists(out_fc_archive):
                    count -= 1
                    print "Archived: {0} because it was removed remaining {1}".format(out_fc_archive, count)
                    arcpy.CopyFeatures_management(archive_fc, out_fc_archive)
                    arcpy.Delete_management(archive_fc)

        except KeyError:
            pass


start_time = datetime.datetime.now()
print "Start Time: " + start_time.ctime()


remove_species, grouplist, proceed = extract_info_master(masterlist_current, masterlist_old)

while proceed:
    archive_location_dict = find_archive_files(grouplist, infolder, skipgroup, remove_species)
    list_archive = archive_location_dict.keys()
    print list_archive
    if len(list_archive) == 0:
        'There are no species that have been removed from list with a file to be archived'
    else:
        archive_dup_files(archive_location_dict, archivefolder, list_archive, archive_date)
    break

end = datetime.datetime.now()
print "End Time: " + end.ctime()

elapsed = end - start_time
print "Elapsed  Time: " + str(elapsed)
