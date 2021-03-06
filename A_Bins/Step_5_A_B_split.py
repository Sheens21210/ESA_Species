# Author: J. Connolly: updated 6/1/2017
# ##############General notes
# All hard coded columns are purposefully, these are new columns used for tracking
# This script will apply the a/b splits to the huc2 a/b based on precipitation data with guidance from the team
# input a_b split table generated by Step_A1_split_HUC2_A_B and Step_A2_splitHUC2_A_B_Summarize
# HUC2 that were modelled in the PWC using multiple MET stations due to precipitation difference across the HUC

# ******** When loading in tables that have huc12 the leading 0 is often dropped.  Must set column as str and updated to
#  include the 0***********

# ############## ASSUMPTIONS
# Col order has not changed since step 1
# Long bin table is used a master for entity id and huc2 header names
# Master huc12/ab split is used for huc12 header names
# Col header in long bin table should be used as output header for final data frame
import pandas as pd
import os
import datetime
import sys


# ################  User input variables
# location where out table will be saved - INPUT Source user
table_folder = r'C:\Users\JConno02\Documents\Projects\ESA\Bins\updates\Script_Check_20170627'

# HUC A/B crosswalk generated by Step_A1_splitHUC2_A_B and Step_A2_Step_A2_splitHUC2_A_B_Summarize
# Place HUC A/B crosswalk into the archive folder for tracking found at table_folder
in_split_nm = 'AllHUC_a_b.csv'

# Species HUC 12 crosswalk generated by Step_B1_GenerateHUC12_Crosswalk
# Place HUC 12 crosswalk into the archive folder for tracking found at table_folder
huc12_col_s = 'HUC_12'  # column header species HUC_12 in_split
huc2_col_s = 'HUC_2'  # column header species HUC_2 in_split
a_b_col_s = 'HUC_Split'  # column header a or b in_split

huc_12_cross_nm = 'R_AllSpe_FWS_NMFS_ByHUC12_20170328.txt'
entity_id_col_cw = 'EntityID'  # column header species EntityID in_split
huc12_col_cw = 'HUC12'  # column header species HUC_12 in_split

# LongBins_[date].csv from Step_4_Transform_binTable_long; file should already be located at the
# path table_folder
long_bins_nm = 'LongBins_20170627.csv'
entity_id_col_c = 'EntityID'  # column header species EntityID long_bins
huc2_col_c = 'HUC_2'  # column header species HUC_2 long_bins

l48_huc_split = ['10', '11', '12', '15', '16', '17', '18']  # L48 HUC2s with an A/B Split
nl48_huc_split = ['19', '20']  # NL48 with an A/B

# ############# Static input variables
today = datetime.datetime.today()
date = today.strftime('%Y%m%d')

huc_split = list(l48_huc_split)
huc_split.extend(nl48_huc_split)
HUC2_Dict = {}
a_b_v = ['a', 'b']

for value in l48_huc_split:
    for i in a_b_v:
        key = value + i
        HUC2_Dict[key] = value

archived_location = table_folder + os.sep + 'Archived'
os.mkdir(archived_location) if not os.path.exists(archived_location) else None
out_table = archived_location + os.sep + 'LongBins_unfiltered_AB_' + str(date) + '.csv'
working_table_L48 = archived_location + os.sep + 'Working_L48_AB_' + str(date) + '.csv'
working_table_NL48 = archived_location + os.sep + 'Working_NL48_AB_' + str(date) + '.csv'

long_bins = archived_location + os.sep + long_bins_nm
in_split = archived_location + os.sep + in_split_nm
huc_12_cross = archived_location + os.sep + huc_12_cross_nm


def update_columns(current_col, updated_col, list_of_col):
    # VARS: current:current_col: value in current list, updated_col: value it should be updated to, list_of_col: list of
    # values
    # DESCRIPTION: Standardize column headers using the current_bin_table header values as the master
    # RETURN: Update list of value used to update column headers

    if current_col != updated_col:
        loc = list_of_col.index(str(current_col))
        list_of_col.remove(str(current_col))
        list_of_col.insert(loc, str(updated_col))
        return list_of_col
    else:
        return list_of_col


def load_data(split, cross, bins_long):
    # VARS: split: HUC_12 a/b split done based on precipitation, cross: species/huc12 crosswalk; long: specie bins
    # assignment long format from Step_4_Transform_binTable_long
    # DESCRIPTION: removes columns without headers from all data frames; sets entity id col as str in all tables with
    # entity id; Verifies entity id, huc2 and huc 12 have the same column headers across tables, match entity id and
    # huc 2 to long bin table, and huc 12 to the master a/b split table. Verifies hard coded columns are
    # found in tables. Try/Excepts makes sure we have a complete archive of data used for update, and intermediate
    # tables.
    # RETURN: data frames of inputs tables; KEY col headers standardize
    try:
        long_df = pd.read_csv(bins_long, dtype=object)
    except IOError:
        print('\nYou must move the long bin table to the table_folder location')
        sys.exit()
    [long_df.drop(v, axis=1, inplace=True) for v in long_df.columns.values.tolist() if v.startswith('Unnamed')]
    long_df[str(entity_id_col_c)] = long_df[str(entity_id_col_c)].map(lambda x: x).astype(str)
    long_df[str(huc2_col_c)] = long_df[str(huc2_col_c)].map(lambda x: x).astype(str)
    cols = long_df.columns.values.tolist()

    try:
        split_df = pd.read_csv(split, dtype=object)
    except IOError:
        print('\nYou must move the master huc12 a/b split table to the archive folder at the table_folder location')
        sys.exit()
    [split_df.drop(v, axis=1, inplace=True) for v in split_df.columns.values.tolist() if v.startswith('Unnamed')]

    split_df_cols = split_df.columns.values.tolist()
    split_df_cols = update_columns(str(huc2_col_s), str(huc2_col_c), split_df_cols)
    split_df.columns = split_df_cols

    try:
        cross_df = pd.read_csv(cross, dtype=object)
    except IOError:
        print('\nYou must move the master species huc12 crosswalk to the archive folder at the table_folder location')
        sys.exit()
    [cross_df.drop(v, axis=1, inplace=True) for v in cross_df.columns.values.tolist() if v.startswith('Unnamed')]
    cross_df[str(entity_id_col_cw)] = cross_df[str(entity_id_col_cw)].map(lambda x: x).astype(str)
    cross_df_cols = cross_df.columns.values.tolist()
    cross_df_cols = update_columns(str(entity_id_col_cw), str(entity_id_col_c), cross_df_cols)
    cross_df_cols = update_columns(str(huc12_col_cw), str(huc12_col_s), cross_df_cols)
    cross_df.columns = cross_df_cols

    return split_df, cross_df, long_df, cols


def a_b_huc12(split_df):
    # VARS: split_df: data frame of the master huc12 a/b splits from in_split
    # DESCRIPTION: sets huc2 and huc12 col as str and verifies that all 12 digits are included in the huc12. Adds
    # column['A_B'] that is the huc2 identifier with the a/b added for each huc12 then runs a group by to group table by
    # this columns.  The groups would included only those huc12 in the huc2_a_b.  Each group is loaded into the
    # dictionary as a value with the key being the huc2_a_b

    # RETURN: dictionary of the huc12 in each a/b split huc2
    huc_a_b_split = {}
    split_df[str(huc12_col_s)] = split_df[str(huc12_col_s)].map(lambda x: str(x))
    split_df[str(huc12_col_s)] = split_df[str(huc12_col_s)].map(lambda x: '0' + x if len(x) == 11 else x).astype(str)
    split_df[str(huc2_col_c)] = (split_df[str(huc2_col_c)].map(lambda x: x[:2]))

    split_df['A_B'] = split_df[str(huc2_col_c)] + split_df[a_b_col_s]
    grouped = split_df.groupby(['A_B'])
    huc_2_splits = grouped.groups.keys()
    for z in huc_2_splits:
        huc_2_df = grouped.get_group(z)
        huc_a_b_split[z] = huc_2_df

    # a small number of HUC12 are flagged as HUC2 9 due to borders, these need to be removed for the
    # purposes this assignment; there is not a/b split in HUC9
    huc_a_b_split.pop('09a', None)
    huc_a_b_split.pop('9a', None)
    return huc_a_b_split


def assign_a_b(row):
    # VARS: row: row of data being updated (apply function to value in HUC_2 column to include the a or b if needed)
    # with bin codes
    # DESCRIPTION: Pulls the result of the A/B split from the HUC_Split_Value column, this will be a, b or no.  If it is
    # a or b this the letter is concatenated to the huc2 identifier and returned, if it is no, just the huc2 identifier
    # is returned

    # RETURN: updated values for column being updated by apply function
    huc_2 = str(row[str(huc2_col_c)])
    a_b = str(row['HUC_Split_Value'])
    if a_b == 'No':
        new_val = huc_2
    else:
        new_val = huc_2 + a_b
    return new_val


def species_a_b(huc_2_a_b_dict, species_list, cross_dict, long_df):
    # VARS: huc_2_a_b_dict: dictionary of huc12s by huc2 with a_b split, species_list: list of species, cross_dict:
    # dictionary huc 12 in species range by entity id, long_df: species bin assignment in long format
    # DESCRIPTION: Long df is filtered to include huc2 with an a/b split in l48. For each species/ huc2 combo compares
    # the huc12s where the species is found to the huc 12 in the huc2 a_b splits.  The ['A'] ['B'] are populated with an
    # a or b if the species is found in that part of the huc2. Df is then melted on the ['A','B'] columns so there is
    # one row per species/huc/a_b split. The a or b is added the huc2 identifier.  Any huc2 identifier without and a or
    # b can be filtered out because the species was not found in both the a and b are of the huc2.
    # RETURN: data frame of just the l48 species found in huc2 with an a/b split, with huc2 identifier that include the
    # a or b

    long_df['Value'].fillna('NAN', inplace=True)
    l48_split_df = long_df.loc[long_df[str(huc2_col_c)].isin(l48_huc_split)]
    cols = l48_split_df.columns.values.tolist()
    cols.extend(['A', 'B'])
    l48_df = l48_split_df.reindex(columns=cols)
    list_a_b_hucs = huc_2_a_b_dict.keys()

    for species in species_list:
        list_spe_huc = (cross_dict[species])
        try:
            list_spe_huc = list_spe_huc[0].split(",")
        except AttributeError:
            list_spe_huc = []
        for a_b in list_a_b_hucs:
            a_or_b = a_b[-1:].capitalize()
            huc2 = HUC2_Dict[a_b]
            a_b_df = huc_2_a_b_dict[a_b]
            a_b_df_filter = (a_b_df.loc[a_b_df['A_B'] == a_b])
            list_spe_huc_filter = [huc12 for huc12 in list_spe_huc if huc12[:2] == huc2]
            if len(a_b_df_filter.loc[a_b_df_filter[str(huc12_col_s)].isin(list_spe_huc_filter)]) != 0:
                l48_df.loc[(l48_df[str(entity_id_col_c)] == species) & (l48_df[str(huc2_col_c)] == huc2), a_or_b] = \
                    a_or_b.lower()
            else:
                pass

    id_vars_lst = l48_df.columns.values.tolist()
    id_vars_lst.remove('A')
    id_vars_lst.remove('B')

    # Transforms DataFrame from wide to long where one or more columns are identifier variables (id_vars), while all
    # other columns, considered measured variables (value_vars), are 'unpivoted' to the row axis, leaving just two
    # non-identifier columns,'variable' and 'value'

    df = pd.melt(l48_df, id_vars=id_vars_lst, value_vars=['A', 'B'], var_name='HUC_Split', value_name='HUC_Split_Value')
    df['HUC_Split_Value'].fillna('No', inplace=True)
    df[str(huc2_col_c)] = df.apply(lambda row: assign_a_b(row), axis=1)
    # filters out the rows of data where the huc2 identifier does not include the a/b assignment; just the original huc2
    df = df.loc[~df[str(huc2_col_c)].isin(l48_huc_split)]

    return list_a_b_hucs, df


def split_long_df(long_df):
    # VARS: huc_2_a_b_dict: dictionary of huc12s by huc2 with a_b split, species_list: list of species, cross_dict:
    # dictionary huc 12 in species range by entity id, long_df: species bin assignment in long format
    # DESCRIPTION: Long df is filtered to include huc2 in nl48.  All huc have all species, and all species are places
    # in both   The ['A'] ['B'] are populated with an a or b Df is then melted on the ['A','B'] columns so there is
    # one row per species/huc/a_b split. The a or b is added the huc2 identifier.
    # RETURN: data frame of just the nl48 species found in huc2 with an a/b split

    nl48_split_df = long_df.loc[long_df[huc2_col_c].isin(nl48_huc_split)]
    cols = nl48_split_df.columns.values.tolist()
    cols.extend(['A', 'B'])
    nl48_df = nl48_split_df.reindex(columns=cols)

    nl48_df['A'].fillna('a', inplace=True)
    nl48_df['B'].fillna('b', inplace=True)

    id_vars_lst = nl48_df.columns.values.tolist()
    id_vars_lst.remove('A')
    id_vars_lst.remove('B')

    # Transforms DataFrame from wide to long where one or more columns are identifier variables (id_vars), while all
    # other columns, considered measured variables (value_vars), are 'unpivoted' to the row axis, leaving just two
    # non-identifier columns,'variable' and 'value'
    df = pd.melt(nl48_split_df, id_vars=id_vars_lst, value_vars=['A', 'B'], var_name='HUC_Split',
                 value_name='HUC_Split_Value')

    df['HUC_Split_Value'].fillna('No', inplace=True)
    df[huc2_col_c] = df.apply(lambda row: assign_a_b(row), axis=1)

    return df


# Time tracker
start_script = datetime.datetime.now()
print "Start Time: " + start_script.ctime()

# Step 1: Load data from bin table long format, removed unnamed columns. Try/Excepts makes sure we have a complete
# archive of data used for update,and intermediate tables.
df_split, df_cross, df_long, final_cols = load_data(in_split, huc_12_cross, long_bins)

# Step 2: Set up dictionaries used for a/b assignments. dict_a_b_split is a dictionary by huc2 including the a/b
# assignments, ie there is 17a and 17b not 17, key is the huc_2, values is a data frame and the huc_12_crosswalk_dict is
# a dictionary of all huc12 in a species range; key is the entity id value HUC12s
dict_a_b_split = a_b_huc12(df_split)
huc_12_crosswalk_dict = df_cross.set_index(str(entity_id_col_c)).T.to_dict('list')
list_species = huc_12_crosswalk_dict.keys()

# Step 3: Compares species huc 12 crosswalk to master huc12  a/b split crosswalk to see if a species is found in a, b or
# both for hucs in the l48
# Working_L48_AB_[date].csv  # just the l48 species with the A/B splits
hucs_a_b, working_df = species_a_b(dict_a_b_split, list_species, huc_12_crosswalk_dict, df_long)
working_df.to_csv(working_table_L48)

# Step 4: For nl48 HUC2 all species are placed in both the a and b huc2, function places each species in these  huc2s
# into both a and b
# Working_NL48_AB_[date].csv  # just the nl48 species with the A/B splits
df_working_nl48 = split_long_df(df_long)
df_working_nl48.to_csv(working_table_NL48)

# Step 5: Merge the l48 and nl48 a/b split data frames with the remaining data for the hucs in the l48 w/o an a_b split
# append is the same as concat bu can only add data along axis=0 ie rows
l48_nl48_df = working_df.append(df_working_nl48)
reindex_cols = df_long.columns.values.tolist()
l48_nl48_df = l48_nl48_df.reindex(columns=final_cols)
non_split_hucs = df_long.loc[~df_long[huc2_col_c].isin(huc_split)]
df_final = non_split_hucs.append(l48_nl48_df)
df_final = df_final.reindex(columns=final_cols)
df_final.drop_duplicates(inplace=True)

# Step 6:Exports transformed data frame to csv
# LongBins_unfiltered_AB_[date].csv  #  long table with a/b split and all bin assignments
df_final.to_csv(out_table, encoding='utf-8')

# Elapsed time
print "Script completed in: {0}".format(datetime.datetime.now() - start_script)
