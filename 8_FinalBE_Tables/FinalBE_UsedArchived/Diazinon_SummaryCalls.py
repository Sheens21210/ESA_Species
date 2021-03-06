import pandas as pd
import datetime

in_range_table = 'E:\Tabulated_NewComps\FinalBETables\DraftNewFormat\R_FinalBE_DiazinonOverlap_20170117.csv'
in_ch_table = 'E:\Tabulated_NewComps\FinalBETables\DraftNewFormat\CH_FinalBE_DiazinonOverlap_20170117.csv'
out_csv_unformat = 'E:\Tabulated_NewComps\FinalBETables\DraftNewFormat\Diazinon_SummaryCalls_20170117_unformated.csv'
out_csv= 'E:\Tabulated_NewComps\FinalBETables\DraftNewFormat\Diazinon_SummaryCalls_20170117.csv'
sp_index_cols = 16

col_list = ['EntityID', 'comname_x', 'sciname_x', 'family_x', 'status_text_x', 'pop_abbrev_x',
            'Group_x', 'Des_CH_x', 'Critical_Habitat__x', 'CH_GIS_x', 'Migratory_x',
            'Range_Overlap_Result', 'Range_Overlap_Result_Comment', 'CH_Overlap_Result', 'CH_Overlap_Result_Comment',
            'Compare R_CH Result', 'R Comment', 'CH Comment']


def add_result_final_table(row, column):
    return row[column]


def clean_source_call_range(row):
    if row['Step 1 ED'] == 'NE':
        return row['Step 1 ED Comment']
    elif row['Step 2 ED'] == 'NLAA':
        if row['Step 2 ED Comment'] == 'NLAA-QualReport':
            return row['Source of Call final BE-Range']
        else:
            return row['Step 2 ED Comment']
    else:

        return row['Source of Call final BE-Range']


def clean_source_call_CH(row):
    if row['CH_Step 1 ED'] == 'NE':
        return row['CH_Step 1 ED Comment']
    elif row['CH_Step 2 ED'] == 'NLAA':
        if row['CH_Step 2 ED Comment'] == 'NLAA-QualReport':
            return row['Source of Call final BE-CH']
        else:
            return row['CH_Step 2 ED Comment']
    else:
        return row['Source of Call final BE-CH']


start_time = datetime.datetime.now()
print "Start Time: " + start_time.ctime()

range_table_df = pd.read_csv(in_range_table)
ch_table_df = pd.read_csv(in_ch_table)
sp_info_df = range_table_df.iloc[:, :sp_index_cols]
print sp_info_df.columns.values.tolist()
range_short = range_table_df.reindex(
    columns=['EntityID', 'Step 1 ED', 'Step 1 ED Comment', 'Step 2 ED', 'Step 2 ED Comment'])
ch_short = ch_table_df.reindex(
    columns=['EntityID', 'Step 1 ED', 'Step 1 ED Comment', 'Step 2 ED', 'Step 2 ED Comment'])
ch_short.columns = ['EntityID', 'CH_Step 1 ED', 'CH_Step 1 ED Comment', 'CH_Step 2 ED', 'CH_Step 2 ED Comment']

merge_df = pd.merge(sp_info_df, range_short, on='EntityID', how='outer')
merge_df = pd.merge(merge_df, ch_short, on='EntityID', how='outer')
merge_df['Source of Call final BE-Range'] = merge_df.apply(lambda row: clean_source_call_range(row), axis=1)
merge_df['Source of Call final BE-CH'] = merge_df.apply(lambda row: clean_source_call_CH(row), axis=1)
print merge_df.columns.values.tolist()
clean_df = merge_df.ix[:,['EntityID', 'comname', 'sciname', 'Source of Call final BE-Range', 'WoE Summary Group', 'Source of Call final BE-CH',  'Step 2 ED',  'CH_Step 2 ED', ]]
clean_df =clean_df.reindex(
    columns=['WoE Summary Group', 'sciname', 'comname', 'EntityID', 'Source of Call final BE-Range', 'Step 2 ED',
             'Source of Call final BE-CH', 'CH_Step 2 ED'])
clean_df.columns = ['Taxa', 'Scientific Name', 'Common Name', 'EntityID1',
                    'Source of Species Effects Determination2', 'Species Call?',
                    'Source of Critical Habitat Effects Determination2', 'Critical Habitat Call?'
                    ]

merge_df.to_csv(out_csv_unformat)
clean_df.to_csv(out_csv)



end = datetime.datetime.now()
print "End Time: " + end.ctime()
elapsed = end - start_time
print "Elapsed  Time: " + str(elapsed)
